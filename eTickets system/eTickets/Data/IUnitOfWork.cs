using eTickets.Data.Interfaces;

namespace eTickets.Data
{
    public interface IUnitOfWork : IDisposable
    {
        IActorRepository Actors { get; }
        IProducerRepository Producers { get; }
        ICinemaRepository Cinemas { get; }
        IMovieRepository Movies { get; }
        IActorMovieRepository Actor_Movies { get; }
        IOrderRepository Orders { get; }
        IOrderItemRepository OrderItems { get; }
        Task CommitAsync();
        Task RollbackAsync();
    }
}
