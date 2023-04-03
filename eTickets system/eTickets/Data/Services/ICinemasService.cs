using eTickets.Models;

namespace eTickets.Data.Services;

public interface ICinemasService
{
    Task<IEnumerable<Cinema>> GetAllCinemas();
    Task<Cinema> GetCinemaById(int id);
    Task AddCinema(Cinema cinema);
    Task UpdateCinema(int id, Cinema cinema);
    Task DeleteCinema(int id);
}
