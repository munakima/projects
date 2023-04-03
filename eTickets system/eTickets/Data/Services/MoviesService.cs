using eTickets.Data.ViewModels;
using eTickets.Models;

namespace eTickets.Data.Services
{
    public class MoviesService : IMoviesService
    {
        private readonly IUnitOfWork _unitOfWork;
        public MoviesService(IUnitOfWork unitOfWork)
        {
            _unitOfWork = unitOfWork;
        }

        public async Task<IEnumerable<Movie>> GetAllMovies() => await _unitOfWork.Movies.GetAllAsync(n => n.Cinema);

        public async Task AddNewMovieAsync(MovieViewModel data) => await _unitOfWork.Movies.AddNewMovieAsync(data);


        public async Task<Movie> GetMovieByIdAsync(int id) => await _unitOfWork.Movies.GetMovieInfo(id);

        public Task<MovieDropdownViewModel> GetNewMovieDropdownsValues() => _unitOfWork.Movies.GetNewMovieDropdownsValues();

        public Task UpdateMovieAsync(MovieViewModel data) => _unitOfWork.Movies.UpdateMovieAsync(data);

        public async Task DeleteMovieAsync(int id)
        {
            await _unitOfWork.Actor_Movies.DeleteAsync(id);
            await _unitOfWork.CommitAsync();
            await _unitOfWork.Movies.DeleteAsync(id);
            await _unitOfWork.CommitAsync();
        }
    }
}
