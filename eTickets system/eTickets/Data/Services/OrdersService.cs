using eTickets.Models;

namespace eTickets.Data.Services
{
    public class OrdersService : IOrdersService
    {
        private readonly IUnitOfWork _unitOfWork;
        public OrdersService(IUnitOfWork unitOfWork)
        {
            _unitOfWork = unitOfWork;
        }

        public async Task<List<Order>> GetOrdersByUserIDAsync(string userId)
        {
            return await _unitOfWork.Orders.GetOrdersByUserIDAsync(userId);
        }

        public async Task StoreOrderAsync(List<ShoppingCartItem> items, string userId, string email)
        {
            var order = _unitOfWork.Orders.AddOrderAsync(userId, email);
            await _unitOfWork.CommitAsync();
            await _unitOfWork.OrderItems.AddOrderItemAsync(items, order);
            await _unitOfWork.CommitAsync();
        }
    }
}