using eTickets.Data.Base;
using eTickets.Data.ViewModels;
using eTickets.Models;

namespace eTickets.Data.Interfaces
{
    public interface IMovieRepository : IEntityBaseRepository<Movie>
    {
        Task<Movie> GetMovieInfo(int id);
        Task<MovieDropdownViewModel> GetNewMovieDropdownsValues();
        Task UpdateMovieAsync(MovieViewModel data);
        Task AddNewMovieAsync(MovieViewModel data);
    }
}
