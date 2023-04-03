using eTickets.Data.Base;
using eTickets.Data.Interfaces;
using eTickets.Models;

namespace eTickets.Data.Repositories
{
    public class ProducerRepository : EntityBaseRepository<Producer>, IProducerRepository
    {
        public ProducerRepository(AppDbContext context) : base(context)
        {
        }

    }
}
