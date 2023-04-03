using eTickets.Data.Base;
using eTickets.Data.Interfaces;
using eTickets.Models;

namespace eTickets.Data.Repositories
{
    public class CinemaRepository : EntityBaseRepository<Cinema>, ICinemaRepository
    {
        public CinemaRepository(AppDbContext context) : base(context)
        {
        }
    }
}
