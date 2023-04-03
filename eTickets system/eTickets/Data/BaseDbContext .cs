using Microsoft.EntityFrameworkCore;

namespace eTickets.Data
{
    public class BaseDbContext : DbContext
    {
        public BaseDbContext(DbContextOptions<BaseDbContext> options) : base(options)
        {
        }
    }
}
