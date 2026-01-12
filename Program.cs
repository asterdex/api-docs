using System;
using System.Threading.Tasks;

public class Program
{
    public static async Task Main(string[] args)
    {
        Console.Write("Enter your API Key: ");
        string apiKey = Console.ReadLine();

        Console.Write("Enter your API Secret: ");
        string apiSecret = Console.ReadLine();

        var exchange = new AsterExchange();

        string symbol = "BTCUSDT"; // Default symbol

        Console.WriteLine("\nChoose an action:");
        Console.WriteLine("1. Place a Buy Order (with 1% Stop-Loss)");
        Console.WriteLine("2. Place a Sell Order");
        Console.Write("Enter your choice (1 or 2): ");
        string choice = Console.ReadLine();

        if (choice == "1")
        {
            Console.Write($"Enter quantity for {symbol}: ");
            decimal buyQuantity = decimal.Parse(Console.ReadLine());
            Console.Write($"Enter price for {symbol}: ");
            decimal buyPrice = decimal.Parse(Console.ReadLine());

            Console.WriteLine($"\nPlacing a buy order for {buyQuantity} {symbol} at {buyPrice} with a 1% stop-loss...");

            var buyResponses = await exchange.PlaceBuyOrder(apiKey, apiSecret, symbol, buyQuantity, buyPrice);

            foreach (var response in buyResponses)
            {
                if (response.Success)
                {
                    Console.WriteLine("Order placed successfully!");
                    Console.WriteLine($"Response Data: {response.Data}");
                }
                else
                {
                    Console.WriteLine($"Failed to place order: {response.Message}");
                }
            }
        }
        else if (choice == "2")
        {
            Console.Write($"Enter quantity for {symbol}: ");
            decimal sellQuantity = decimal.Parse(Console.ReadLine());
            Console.Write($"Enter price for {symbol}: ");
            decimal sellPrice = decimal.Parse(Console.ReadLine());

            Console.WriteLine($"\nPlacing a sell order for {sellQuantity} {symbol} at {sellPrice}...");

            var sellResponse = await exchange.PlaceSellOrder(apiKey, apiSecret, symbol, sellQuantity, sellPrice);

            if (sellResponse.Success)
            {
                Console.WriteLine("Order placed successfully!");
                Console.WriteLine($"Response Data: {sellResponse.Data}");
            }
            else
            {
                Console.WriteLine($"Failed to place order: {sellResponse.Message}");
            }
        }
        else
        {
            Console.WriteLine("Invalid choice.");
        }
    }
}
