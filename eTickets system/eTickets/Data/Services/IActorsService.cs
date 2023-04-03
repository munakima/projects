using eTickets.Models;

namespace eTickets.Data.Services;

public interface IActorsService
{
    Task<IEnumerable<Actor>> GetAllActors();
    Task<Actor> GetActorById(int id);
    Task AddActor(Actor actor);
    Task UpdateActor(int id, Actor actor);
    Task DeleteActor(int id);
}
