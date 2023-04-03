using eTickets.Models;

namespace eTickets.Data.Services
{
    public interface IOrdersService
    {
        public Task StoreOrderAsync(List<ShoppingCartItem> items, string userId, string email);
        public Task<List<Order>> GetOrdersByUserIDAsync(string userId);
    }
}
