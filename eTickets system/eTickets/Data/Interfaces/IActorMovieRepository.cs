using eTickets.Models;

namespace eTickets.Data.Interfaces
{
    public interface IActorMovieRepository
    {
        Task AddAsync(Actor_Movie entity);
        Task DeleteAsync(int id);
    }
}
