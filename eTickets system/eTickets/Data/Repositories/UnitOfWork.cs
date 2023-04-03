using eTickets.Data.Interfaces;

namespace eTickets.Data.Repositories
{
    public class UnitOfWork : IUnitOfWork
    {
        private readonly AppDbContext _context;

        public IActorRepository Actors { get; }
        public IProducerRepository Producers { get; }
        public ICinemaRepository Cinemas { get; }
        public IMovieRepository Movies { get; }
        public IActorMovieRepository Actor_Movies { get; }
        public IOrderRepository Orders { get; }
        public IOrderItemRepository OrderItems { get; }

        public UnitOfWork(AppDbContext context, IActorRepository actorRepository,
            IProducerRepository producerRepository, ICinemaRepository cinemaRepository
            , IMovieRepository movies, IActorMovieRepository actor_Movies,
            IOrderRepository orders, IOrderItemRepository orderItems)
        {
            _context = context;
            Actors = actorRepository;
            Producers = producerRepository;
            Cinemas = cinemaRepository;
            Movies = movies;
            Actor_Movies = actor_Movies;
            Orders = orders;
            OrderItems = orderItems;
        }

        public void Dispose()
        {
            Dispose(true);
            GC.SuppressFinalize(this);
        }

        public void Dispose(bool disposing)
        {
            if (disposing)
            {
                _context.Dispose();
            }
        }

        public async Task CommitAsync()
        {
            await _context.SaveChangesAsync();
        }

        public async Task RollbackAsync()
            => await _context.DisposeAsync();
    }
}
