using eTickets.Data.Interfaces;
using eTickets.Models;

namespace eTickets.Data.Repositories
{
    public class OrderItemRepository : IOrderItemRepository
    {
        private readonly AppDbContext _context;

        public OrderItemRepository(AppDbContext context)
        {
            _context = context;
        }
        public async Task AddOrderItemAsync(List<ShoppingCartItem> items, Task<Order> order)
        {

            items.ForEach(async item =>
            {
                var orderItem = new OrderItem()
                {
                    Quantity = item.Qauntity,
                    MovieId = item.Movie.Id,
                    OrderId = order.Id,
                    Price = item.Movie.Price,
                };
            });
        }
    }
}
