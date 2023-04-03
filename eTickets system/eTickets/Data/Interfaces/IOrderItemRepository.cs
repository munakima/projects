using eTickets.Models;

namespace eTickets.Data.Interfaces
{
    public interface IOrderItemRepository
    {
        Task AddOrderItemAsync(List<ShoppingCartItem> items, Task<Order> order);
    }
}
