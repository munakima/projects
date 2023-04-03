using eTickets.Data.ViewModels;
using eTickets.Models;

namespace eTickets.Data.Services
{
    public interface IMoviesService
    {
        Task<IEnumerable<Movie>> GetAllMovies();
        Task<Movie> GetMovieByIdAsync(int id);
        Task<MovieDropdownViewModel> GetNewMovieDropdownsValues();
        Task AddNewMovieAsync(MovieViewModel data);
        Task UpdateMovieAsync(MovieViewModel data);
        Task DeleteMovieAsync(int id);
    }
}
