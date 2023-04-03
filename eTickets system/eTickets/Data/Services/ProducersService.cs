using eTickets.Models;

namespace eTickets.Data.Services
{
    public class ProducersService : IProducersService
    {
        private readonly IUnitOfWork _unitOfWork;
        public ProducersService(IUnitOfWork unitOfWork)
        {
            _unitOfWork = unitOfWork;
        }
        public async Task AddProducer(Producer producer)
        {
            await _unitOfWork.Producers.AddAsync(producer);
            await _unitOfWork.CommitAsync();
        }

        public async Task DeleteProducer(int id)
        {
            await _unitOfWork.Producers.DeleteAsync(id);
            await _unitOfWork.CommitAsync();
        }

        public async Task<IEnumerable<Producer>> GetAllProducers() => await _unitOfWork.Producers.GetAllAsync();

        public async Task<Producer> GetProducerById(int id) => await _unitOfWork.Producers.GetByIdAsync(id);

        public async Task UpdateProducer(int id, Producer producer)
        {
            await _unitOfWork.Producers.UpdataAsync(id, producer);
            await _unitOfWork.CommitAsync();
        }
    }
}
