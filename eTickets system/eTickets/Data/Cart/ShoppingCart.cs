using eTickets.Models;
using Microsoft.EntityFrameworkCore;

namespace eTickets.Data.Cart
{
    public class ShoppingCart
    {
        private readonly AppDbContext _context;

        public string ShoppingCartId { get; set; }
        public List<ShoppingCartItem> ShoppingCartItems { get; set; }

        public ShoppingCart(AppDbContext context)
        {
            _context = context;
        }

        public static ShoppingCart GetShoppingCart(IServiceProvider service)
        {
            ISession session = service.GetRequiredService<IHttpContextAccessor>()?.HttpContext.Session;
            var context = service.GetService<AppDbContext>();
            var cartId = session.GetString("CartId") ?? Guid.NewGuid().ToString();
            session.SetString("CartId", cartId);
            return new ShoppingCart(context) { ShoppingCartId = cartId };
        }

        public async Task AddItemToCart(Movie movie)
        {
            var shoppingCartItem = await _context.ShoppingCartItems.FirstOrDefaultAsync(item => item.Movie.Id == movie.Id &&
                item.ShoppingCartId == ShoppingCartId);

            if (shoppingCartItem != null)
            {
                shoppingCartItem.Qauntity++;
            }
            else
            {
                shoppingCartItem = new ShoppingCartItem()
                {
                    ShoppingCartId = ShoppingCartId,
                    Movie = movie,
                    Qauntity = 1,
                };
                await _context.ShoppingCartItems.AddAsync(shoppingCartItem);
            }
            await _context.SaveChangesAsync();
        }

        public async Task RemoveItemFromCart(Movie movie)
        {
            var shoppingCartItem = await _context.ShoppingCartItems.FirstOrDefaultAsync(item => item.Movie.Id == movie.Id &&
                    item.ShoppingCartId == ShoppingCartId);

            if (shoppingCartItem == null)
                return;

            if (shoppingCartItem.Qauntity > 1)
            {
                shoppingCartItem.Qauntity--;
            }
            else
            {
                _context.ShoppingCartItems.Remove(shoppingCartItem);
            }

            await _context.SaveChangesAsync();
        }

        public List<ShoppingCartItem> GetShoppingCartItems()
        {
            return ShoppingCartItems ?? (ShoppingCartItems = _context.ShoppingCartItems
                .Where(n => n.ShoppingCartId == ShoppingCartId)
                .Include(n => n.Movie).ToList());
        }

        public double GetShoppingCartTotal()
        {
            var total = _context.ShoppingCartItems
                .Where(n => n.ShoppingCartId == ShoppingCartId)
                .Select(n => n.Movie.Price * n.Qauntity).Sum();

            return total;
        }

        public async Task ClearShoppingCartAsync()
        {
            var items = ShoppingCartItems ?? (ShoppingCartItems = await _context.ShoppingCartItems
                .Where(n => n.ShoppingCartId == ShoppingCartId)
                .ToListAsync());
            _context.ShoppingCartItems.RemoveRange(items);
            await _context.SaveChangesAsync();
        }
    }
}