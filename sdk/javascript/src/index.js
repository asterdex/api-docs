/**
 * AsterDex JavaScript SDK — Community Edition by Kairos Lab.
 *
 * Handles V3 EIP-712 authentication, nonce management, and all
 * documented + undocumented endpoints.
 *
 * @module @kairoslab/asterdex-sdk
 */

import { ethers } from "ethers";

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

export const MAINNET_BASE = "https://fapi.asterdex.com";
export const TESTNET_BASE = "https://testnet-fapi.asterdex.com";
export const MAINNET_WS = "wss://fstream.asterdex.com";
export const TESTNET_WS = "wss://testnet-fstream.asterdex.com";
export const CHAIN_ID_MAINNET = 1666;
export const CHAIN_ID_TESTNET = 714;

const EIP712_DOMAIN = {
  name: "AsterSignTransaction",
  version: "1",
  chainId: CHAIN_ID_MAINNET,
  verifyingContract: "0x0000000000000000000000000000000000000000",
};

const EIP712_TYPES = {
  Message: [{ name: "msg", type: "string" }],
};

// ---------------------------------------------------------------------------
// Errors
// ---------------------------------------------------------------------------

export class AsterDexError extends Error {
  constructor(code, message, response = null) {
    super(`[${code}] ${message}`);
    this.name = "AsterDexError";
    this.code = code;
    this.response = response;
  }
}

export class AsterDexAuthError extends AsterDexError {
  constructor(code, message, response) {
    super(code, message, response);
    this.name = "AsterDexAuthError";
  }
}

export class AsterDexRateLimitError extends AsterDexError {
  constructor(code, message) {
    super(code, message);
    this.name = "AsterDexRateLimitError";
  }
}

// ---------------------------------------------------------------------------
// Signing
// ---------------------------------------------------------------------------

/**
 * Build sign payload: sort by ASCII key order, join with &.
 * @param {Record<string, any>} params
 * @returns {string}
 */
function buildSignPayload(params) {
  return Object.keys(params)
    .sort()
    .map((key) => {
      let val = params[key];
      if (typeof val === "boolean") val = val.toString().toLowerCase();
      return `${key}=${val}`;
    })
    .join("&");
}

/**
 * Sign a V3 request with EIP-712 typed data.
 * @param {Record<string, any>} params
 * @param {string} user
 * @param {string} signer
 * @param {string} privateKey
 * @param {number} chainId
 * @returns {Promise<Record<string, any>>}
 */
async function signV3(params, user, signer, privateKey, chainId) {
  const nonce = String(Math.floor(Date.now() * 1000)); // microseconds
  const timestamp = String(Date.now());

  const signParams = { ...params, user, signer, nonce };
  const payloadStr = buildSignPayload(signParams);

  const domain = { ...EIP712_DOMAIN, chainId };
  const wallet = new ethers.Wallet(privateKey);
  const signature = await wallet.signTypedData(domain, EIP712_TYPES, {
    msg: payloadStr,
  });

  return {
    ...params,
    user,
    signer,
    nonce,
    timestamp,
    signature,
  };
}

// ---------------------------------------------------------------------------
// Client
// ---------------------------------------------------------------------------

export class AsterDexClient {
  /**
   * @param {Object} options
   * @param {string} [options.user] - Main wallet address
   * @param {string} [options.signer] - Agent/signer address
   * @param {string} [options.privateKey] - Agent private key
   * @param {string} [options.mainPrivateKey] - Main wallet key (for agent/builder ops)
   * @param {string} [options.baseUrl] - API base URL
   * @param {number} [options.chainId] - Chain ID (1666 mainnet, 714 testnet)
   * @param {number} [options.timeout] - Request timeout in ms
   * @param {string} [options.builder] - Builder address for fee sharing
   */
  constructor({
    user = "",
    signer = "",
    privateKey = "",
    mainPrivateKey = "",
    baseUrl = MAINNET_BASE,
    chainId = CHAIN_ID_MAINNET,
    timeout = 10000,
    builder = "",
  } = {}) {
    this.user = user;
    this.signer = signer;
    this.privateKey = privateKey;
    this.mainPrivateKey = mainPrivateKey;
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.chainId = chainId;
    this.timeout = timeout;
    this.builder = builder;
  }

  // ----------------------------------------------------------------
  // Internal HTTP
  // ----------------------------------------------------------------

  /**
   * @private
   */
  async _request(method, path, params = {}, { signed = false, useMainKey = false } = {}) {
    const url = new URL(path, this.baseUrl);

    // Remove undefined/null
    const cleanParams = Object.fromEntries(
      Object.entries(params).filter(([, v]) => v !== undefined && v !== null)
    );

    let finalParams = cleanParams;
    if (signed) {
      const key = useMainKey ? this.mainPrivateKey : this.privateKey;
      if (!key) {
        throw new AsterDexAuthError(
          -1,
          "Private key required for signed requests."
        );
      }
      finalParams = await signV3(
        cleanParams,
        this.user,
        this.signer,
        key,
        this.chainId
      );
    }

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    let resp;
    try {
      if (method === "GET") {
        url.search = new URLSearchParams(finalParams).toString();
        resp = await fetch(url.toString(), {
          method: "GET",
          headers: {
            "User-Agent": `AsterDexSDK-JS/0.1.0`,
          },
          signal: controller.signal,
        });
      } else {
        resp = await fetch(url.toString(), {
          method,
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": `AsterDexSDK-JS/0.1.0`,
          },
          body: new URLSearchParams(finalParams).toString(),
          signal: controller.signal,
        });
      }
    } catch (err) {
      throw new AsterDexError(-1, `Network error: ${err.message}`);
    } finally {
      clearTimeout(timeoutId);
    }

    if (resp.status === 429) {
      throw new AsterDexRateLimitError(429, "Rate limit exceeded");
    }
    if (resp.status === 418) {
      throw new AsterDexRateLimitError(418, "IP banned after rate limit");
    }

    let data;
    try {
      data = await resp.json();
    } catch {
      if (resp.status >= 400) {
        throw new AsterDexError(resp.status, await resp.text());
      }
      return await resp.text();
    }

    if (data && data.code && data.code !== 200) {
      const ErrorClass = [-2015, -1022, -1021].includes(data.code)
        ? AsterDexAuthError
        : AsterDexError;
      throw new ErrorClass(data.code, data.msg || "Unknown error", data);
    }

    return data;
  }

  /** @private */
  async _public(path, params) {
    return this._request("GET", path, params);
  }

  /** @private */
  async _signedGet(path, params) {
    return this._request("GET", path, params, { signed: true });
  }

  /** @private */
  async _signedPost(path, params, { useMainKey = false } = {}) {
    return this._request("POST", path, params, { signed: true, useMainKey });
  }

  /** @private */
  async _signedDelete(path, params, { useMainKey = false } = {}) {
    return this._request("DELETE", path, params, { signed: true, useMainKey });
  }

  // ==================================================================
  // PUBLIC ENDPOINTS
  // ==================================================================

  async ping() {
    return this._public("/fapi/v3/ping");
  }

  async getServerTime() {
    return this._public("/fapi/v3/time");
  }

  async getExchangeInfo() {
    return this._public("/fapi/v3/exchangeInfo");
  }

  async getOrderBook(symbol, limit = 500) {
    return this._public("/fapi/v3/depth", { symbol, limit });
  }

  async getRecentTrades(symbol, limit = 500) {
    return this._public("/fapi/v3/trades", { symbol, limit });
  }

  async getKlines(symbol, interval, { startTime, endTime, limit = 500 } = {}) {
    return this._public("/fapi/v3/klines", {
      symbol,
      interval,
      startTime,
      endTime,
      limit,
    });
  }

  async getMarkPrice(symbol) {
    return this._public("/fapi/v3/premiumIndex", symbol ? { symbol } : {});
  }

  async getFundingRate(symbol, { startTime, endTime, limit = 100 } = {}) {
    return this._public("/fapi/v3/fundingRate", {
      symbol,
      startTime,
      endTime,
      limit,
    });
  }

  async getTicker24hr(symbol) {
    return this._public("/fapi/v3/ticker/24hr", symbol ? { symbol } : {});
  }

  async getTickerPrice(symbol) {
    return this._public("/fapi/v3/ticker/price", symbol ? { symbol } : {});
  }

  async getBookTicker(symbol) {
    return this._public("/fapi/v3/ticker/bookTicker", symbol ? { symbol } : {});
  }

  /** Undocumented — returns one-sided OI in base-asset units. */
  async getOpenInterest(symbol) {
    return this._public("/fapi/v3/openInterest", { symbol });
  }

  // ==================================================================
  // TRADING
  // ==================================================================

  async placeOrder({
    symbol,
    side,
    type,
    quantity,
    price,
    timeInForce,
    reduceOnly,
    stopPrice,
    positionSide,
    newClientOrderId,
  }) {
    const params = {
      symbol,
      side,
      type,
      quantity,
      price,
      timeInForce,
      reduceOnly,
      stopPrice,
      positionSide,
      newClientOrderId,
    };
    if (this.builder) params.builder = this.builder;
    return this._signedPost("/fapi/v3/order", params);
  }

  async cancelOrder(symbol, { orderId, origClientOrderId } = {}) {
    return this._signedDelete("/fapi/v3/order", {
      symbol,
      orderId,
      origClientOrderId,
    });
  }

  async cancelAllOrders(symbol) {
    return this._signedDelete("/fapi/v3/allOpenOrders", { symbol });
  }

  async noop() {
    return this._signedPost("/fapi/v3/noop");
  }

  // ==================================================================
  // ACCOUNT
  // ==================================================================

  async getBalance() {
    return this._signedGet("/fapi/v3/balance");
  }

  async getAccount() {
    return this._signedGet("/fapi/v3/accountWithJoinMargin");
  }

  async getPositions(symbol) {
    return this._signedGet("/fapi/v3/positionRisk", symbol ? { symbol } : {});
  }

  async getOpenOrders(symbol) {
    return this._signedGet("/fapi/v3/openOrders", symbol ? { symbol } : {});
  }

  async getAllOrders(symbol, { orderId, startTime, endTime, limit = 500 } = {}) {
    return this._signedGet("/fapi/v3/allOrders", {
      symbol,
      orderId,
      startTime,
      endTime,
      limit,
    });
  }

  async getUserTrades(symbol, { startTime, endTime, fromId, limit = 500 } = {}) {
    return this._signedGet("/fapi/v3/userTrades", {
      symbol,
      startTime,
      endTime,
      fromId,
      limit,
    });
  }

  async getIncome({ symbol, incomeType, startTime, endTime, limit = 100 } = {}) {
    return this._signedGet("/fapi/v3/income", {
      symbol,
      incomeType,
      startTime,
      endTime,
      limit,
    });
  }

  async getLeverageBrackets(symbol) {
    return this._signedGet("/fapi/v3/leverageBracket", symbol ? { symbol } : {});
  }

  async getCommissionRate(symbol) {
    return this._signedGet("/fapi/v3/commissionRate", { symbol });
  }

  // ==================================================================
  // POSITION & MARGIN
  // ==================================================================

  async changeLeverage(symbol, leverage) {
    return this._signedPost("/fapi/v3/leverage", { symbol, leverage });
  }

  async changeMarginType(symbol, marginType) {
    return this._signedPost("/fapi/v3/marginType", { symbol, marginType });
  }

  async changePositionMode(dualSidePosition) {
    return this._signedPost("/fapi/v3/positionSide/dual", { dualSidePosition });
  }

  async getPositionMode() {
    return this._signedGet("/fapi/v3/positionSide/dual");
  }

  // ==================================================================
  // AGENT & BUILDER (undocumented)
  // ==================================================================

  async approveAgent({
    agentName,
    agentAddress,
    expired,
    canSpotTrade = false,
    canPerpTrade = true,
    canWithdraw = false,
    ipWhitelist = "",
  }) {
    return this._signedPost(
      "/fapi/v3/approveAgent",
      {
        agentName,
        agentAddress,
        ipWhitelist,
        expired,
        canSpotTrade,
        canPerpTrade,
        canWithdraw,
      },
      { useMainKey: true }
    );
  }

  async getAgents() {
    return this._signedGet("/fapi/v3/agent");
  }

  async deleteAgent(agentAddress) {
    return this._signedDelete("/fapi/v3/agent", { agentAddress }, { useMainKey: true });
  }

  async approveBuilder(builderAddress, maxFeeRate, builderName) {
    return this._signedPost(
      "/fapi/v3/approveBuilder",
      { builder: builderAddress, maxFeeRate, builderName },
      { useMainKey: true }
    );
  }

  async getBuilders() {
    return this._signedGet("/fapi/v3/builder");
  }

  async deleteBuilder(builderAddress) {
    return this._signedDelete("/fapi/v3/builder", { builder: builderAddress }, { useMainKey: true });
  }

  // ==================================================================
  // USER DATA STREAM
  // ==================================================================

  async startUserStream() {
    return this._request("POST", "/fapi/v3/listenKey");
  }

  async keepaliveUserStream() {
    return this._request("PUT", "/fapi/v3/listenKey");
  }

  async closeUserStream() {
    return this._request("DELETE", "/fapi/v3/listenKey");
  }
}

export default AsterDexClient;
