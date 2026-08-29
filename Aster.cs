using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

public class OrderResponse
{
    public bool Success { get; set; }
    public string Message { get; set; }
    public JsonElement Data { get; set; }
}

public class AsterExchange
{
    private string Sign(string apiSecret, string stringToSign)
    {
        using (var hmac = new HMACSHA256(Encoding.UTF8.GetBytes(apiSecret)))
        {
            return BitConverter.ToString(hmac.ComputeHash(Encoding.UTF8.GetBytes(stringToSign))).Replace("-", "").ToLower();
        }
    }

    private async Task<OrderResponse> PlaceOrderAsync(string apiKey, string apiSecret, string symbol, decimal quantity, decimal price, string side, string type = "LIMIT", decimal? stopPrice = null)
    {
        using (var client = new HttpClient())
        {
            try
            {
                var request = new HttpRequestMessage(HttpMethod.Post, "https://api.aster.exchange/v3/trade");

                var timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds().ToString();
                var parameters = new SortedDictionary<string, string>
                {
                    { "api_key", apiKey },
                    { "timestamp", timestamp },
                    { "symbol", symbol },
                    { "quantity", quantity.ToString() },
                    { "price", price.ToString() },
                    { "side", side },
                    { "type", type }
                };

                if (stopPrice.HasValue)
                {
                    parameters.Add("stopPrice", stopPrice.Value.ToString());
                }

                var stringToSign = string.Join("&", parameters.Select(kvp => $"{kvp.Key}={kvp.Value}"));
                var signature = Sign(apiSecret, stringToSign);
                parameters.Add("signature", signature);

                request.Content = new FormUrlEncodedContent(parameters);

                var response = await client.SendAsync(request);
                var responseContent = await response.Content.ReadAsStringAsync();

                if (!response.IsSuccessStatusCode)
                {
                    return new OrderResponse { Success = false, Message = $"API Error: {response.StatusCode} - {responseContent}" };
                }

                var parsedResponse = JsonSerializer.Deserialize<JsonElement>(responseContent);
                return new OrderResponse { Success = true, Message = "Order placed successfully.", Data = parsedResponse };
            }
            catch (HttpRequestException ex)
            {
                return new OrderResponse { Success = false, Message = $"Request Error: {ex.Message}" };
            }
        }
    }

    public async Task<List<OrderResponse>> PlaceBuyOrder(string apiKey, string apiSecret, string symbol, decimal quantity, decimal price, decimal stopLossPercentage = 1.0m)
    {
        var responses = new List<OrderResponse>();

        var buyOrderResponse = await PlaceOrderAsync(apiKey, apiSecret, symbol, quantity, price, "BUY");
        responses.Add(buyOrderResponse);

        if (buyOrderResponse.Success)
        {
            var stopPrice = price * (1 - (stopLossPercentage / 100));
            var stopLossResponse = await PlaceStopLossOrder(apiKey, apiSecret, symbol, quantity, stopPrice, stopPrice);
            responses.Add(stopLossResponse);
        }

        return responses;
    }

    public async Task<OrderResponse> PlaceSellOrder(string apiKey, string apiSecret, string symbol, decimal quantity, decimal price)
    {
        return await PlaceOrderAsync(apiKey, apiSecret, symbol, quantity, price, "SELL");
    }

    public async Task<OrderResponse> PlaceStopLossOrder(string apiKey, string apiSecret, string symbol, decimal quantity, decimal price, decimal stopPrice)
    {
        return await PlaceOrderAsync(apiKey, apiSecret, symbol, quantity, price, "SELL", "STOP_LOSS_LIMIT", stopPrice);
    }
}
