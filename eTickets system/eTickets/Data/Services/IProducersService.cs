using eTickets.Models;

namespace eTickets.Data.Services
{
    public interface IProducersService
    {
        Task<IEnumerable<Producer>> GetAllProducers();
        Task<Producer> GetProducerById(int id);
        Task AddProducer(Producer producer);
        Task UpdateProducer(int id, Producer producer);
        Task DeleteProducer(int id);
    }
}
