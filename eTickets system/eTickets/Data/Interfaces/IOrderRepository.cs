using eTickets.Models;

namespace eTickets.Data.Interfaces
{
    public interface IOrderRepository
    {
        Task<List<Order>> GetOrdersByUserIDAsync(string userId);
        Task<Order> AddOrderAsync(string userId, string email);
    }
}
