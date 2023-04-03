using eTickets.Data.Interfaces;
using eTickets.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.ChangeTracking;

namespace eTickets.Data.Repositories
{
    public class ActorMovieRepository : IActorMovieRepository
    {
        private readonly AppDbContext _context;

        public ActorMovieRepository(AppDbContext context)
        {
            _context = context;
        }

        public async Task AddAsync(Actor_Movie entity)
        {
            await _context.Actors_Movies.AddAsync(entity);
        }

        public async Task DeleteAsync(int id)
        {        
            var entity = await _context.Set<Actor_Movie>().FirstOrDefaultAsync(n => n.MovieId == id);
            if (entity == null)
                return;
            EntityEntry entityEntry = _context.Entry<Actor_Movie>(entity);
            entityEntry.State = EntityState.Deleted;
        }
    }
}
