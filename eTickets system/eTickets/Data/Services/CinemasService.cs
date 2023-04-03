using eTickets.Models;

namespace eTickets.Data.Services;

public class CinemasService : ICinemasService
{
    private readonly IUnitOfWork _unitOfWork;
    public CinemasService(IUnitOfWork unitOfWork)
    {
        _unitOfWork = unitOfWork;
    }
    public async Task AddCinema(Cinema cinema)
    {
        await _unitOfWork.Cinemas.AddAsync(cinema);
        await _unitOfWork.CommitAsync();
    }

    public async Task DeleteCinema(int id)
    {
        await _unitOfWork.Cinemas.DeleteAsync(id);
        await _unitOfWork.CommitAsync();
    }

    public async Task<IEnumerable<Cinema>> GetAllCinemas() => await _unitOfWork.Cinemas.GetAllAsync();

    public async Task<Cinema> GetCinemaById(int id) => await _unitOfWork.Cinemas.GetByIdAsync(id);
    public async Task UpdateCinema(int id, Cinema cinema)
    {
        await _unitOfWork.Cinemas.UpdataAsync(id, cinema);
        await _unitOfWork.CommitAsync();
    }
}
