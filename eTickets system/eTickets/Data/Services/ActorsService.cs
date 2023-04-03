using eTickets.Models;

namespace eTickets.Data.Services;

public class ActorsService : IActorsService
{
    private readonly IUnitOfWork _unitOfWork;
    public ActorsService(IUnitOfWork unitOfWork)
    {
        _unitOfWork = unitOfWork;
    }

    public async Task AddActor(Actor actor)
    {
        await _unitOfWork.Actors.AddAsync(actor);
        await _unitOfWork.CommitAsync();
    }

    public async Task DeleteActor(int id)
    {
        await _unitOfWork.Actors.DeleteAsync(id);
        await _unitOfWork.CommitAsync();
    }

    public async Task<Actor> GetActorById(int id) => await _unitOfWork.Actors.GetByIdAsync(id);

    public async Task<IEnumerable<Actor>> GetAllActors() => await _unitOfWork.Actors.GetAllAsync();

    public async Task UpdateActor(int id, Actor actor)
    {
        await _unitOfWork.Actors.UpdataAsync(id, actor);
        await _unitOfWork.CommitAsync();
    }
}

