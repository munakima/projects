using eTickets.Data.Interfaces;
using eTickets.Models;
using Microsoft.EntityFrameworkCore;

namespace eTickets.Data.Repositories
{
    public class OrderRepository : IOrderRepository
    {
        private readonly AppDbContext _context;

        public OrderRepository(AppDbContext context)
        {
            _context = context;
        }

        public async Task<List<Order>> GetOrdersByUserIDAsync(string userId)
        {
            var orders = await _context.Orders
                .Include(n => n.OrderItems)
                .ThenInclude(n => n.Movie)
                .Where(n => n.UserId == userId).ToListAsync();

            return orders;
        }

        public async Task<Order> AddOrderAsync(string userId, string email)
        {
            var order = new Order
            {
                UserId = userId,
                Email = email
            };
            await _context.Orders.AddAsync(order);
            return order;
        }

    }
}
