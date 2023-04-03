using Microsoft.VisualStudio.TestTools.UnitTesting;
using eTickets.Data.Interfaces;
using Moq;
using eTickets.Models;

namespace eTickets.Data.Services.Tests
{
    [TestClass()]
    public class ProducersServiceTests
    {
        private Mock<IProducerRepository> _mockProducerRepository;
        private Mock<IUnitOfWork> _mockUnitOfWork;
        private IProducersService _producersService;

        [TestInitialize]
        public void TestInitialize()
        {
            _mockProducerRepository = new Mock<IProducerRepository>();
            _mockUnitOfWork = new Mock<IUnitOfWork>();
            _mockUnitOfWork.Setup(u => u.Producers).Returns(_mockProducerRepository.Object);

            // initialize ProducersService with mocks
            _producersService = new ProducersService(_mockUnitOfWork.Object);
        }


        [TestMethod]
        [DataTestMethod]
        [DataRow(1)]
        [DataRow(2)]
        public async Task Test_AddProducer_ShouldAddProducerToRepository(int producerId)
        {
            // Arrange
            var producer = ProducerTemplateForTestData(producerId);

            // Act
            await _producersService.AddProducer(producer);

            // Assert
            _mockUnitOfWork.Verify(u => u.Producers.AddAsync(It.Is<Producer>(a => a.Id == producer.Id)), Times.Once);
            _mockUnitOfWork.Verify(u => u.CommitAsync(), Times.Once);
        }

        [TestMethod]
        [DataTestMethod]
        [DataRow(1)]
        [DataRow(2)]
        [DataRow(3)]
        public async Task Test_GetProducerById_ReturnsProducerWithMatchingIdAsync(int producerId)
        {
            // Arrange
            var producer = ProducerTemplateForTestData(producerId);
            _mockProducerRepository.Setup(r => r.GetByIdAsync(producerId)).ReturnsAsync(producer);
            _mockUnitOfWork.Setup(u => u.Producers).Returns(_mockProducerRepository.Object);

            // Act
            var result = await _producersService.GetProducerById(producerId);

            // Assert
            Assert.IsNotNull(result);
            Assert.AreEqual(producer.Id, result.Id);
            Assert.AreEqual(producer.FullName, result.FullName);
            Assert.AreEqual(producer.Bio, result.Bio);
            Assert.AreEqual(producer.ProfilePictureURL, result.ProfilePictureURL);
        }

        [TestMethod]
        public async Task Test_GetAllProducers_ShouldReturnAllProducers()
        {
            // Arrange
            var expectedProducers = InitNewProducers();
            _mockUnitOfWork.Setup(u => u.Producers.GetAllAsync()).ReturnsAsync(expectedProducers);

            // Act
            var actualProducers = await _producersService.GetAllProducers();

            // Assert
            Assert.AreEqual(expectedProducers.Count, actualProducers.ToList().Count);
            Assert.AreEqual(expectedProducers[0].Id, actualProducers.ToList()[0].Id);
            Assert.AreEqual(expectedProducers[1].Id, actualProducers.ToList()[1].Id);
        }

        [TestMethod]
        [DataRow(1)]
        [DataRow(2)]
        public async Task Test_DeleteProducer_DeletesProducerFromRepository(int producerId)
        {
            // Arrange
            _mockProducerRepository.Setup(r => r.DeleteAsync(producerId)).Returns(Task.CompletedTask);
            _mockUnitOfWork.Setup(u => u.Producers).Returns(_mockProducerRepository.Object);

            // Act
            await _producersService.DeleteProducer(producerId);

            // Assert
            _mockProducerRepository.Verify(r => r.DeleteAsync(producerId), Times.Once);
            _mockUnitOfWork.Verify(u => u.CommitAsync(), Times.Once);
        }

        [TestMethod]
        [DataTestMethod]
        [DataRow(1, "Updated Producer Full Name 1", "Test Profile Picture 1", "Updated Bio 1")]
        [DataRow(2, "Updated Producer Full Name 2", "Test Profile Picture 2", "Updated Bio 2")]
        public async Task Test_UpdateProducer_ShouldUpdateProducerInRepository(int producerId, string updatedFullName, string updateProfile, string updatedBio)
        {
            // Arrange
            var producer = ProducerTemplateForTestData(producerId);
            await _producersService.AddProducer(producer);

            // Act
            producer.FullName = updatedFullName;
            producer.Bio = updatedBio;
            producer.ProfilePictureURL = updateProfile;
            await _producersService.UpdateProducer(producerId, producer);

            // Assert
            _mockUnitOfWork.Verify(u => u.Producers.UpdataAsync(producerId, producer), Times.Once);
            _mockUnitOfWork.Verify(u => u.CommitAsync(), Times.AtLeastOnce);
        }


        private List<Producer> InitNewProducers()
        {
            var testProducers = new List<Producer>
            {
                new Producer { Id = 1, FullName = "Test Producer 1", ProfilePictureURL = "Test Profile Picture 1", Bio = "Test Biography 1" },
                new Producer { Id = 2, FullName = "Test Producer 2", ProfilePictureURL = "Test Profile Picture 2", Bio = "Test Biography 2" }
            };
            return testProducers;
        }
        private Producer ProducerTemplateForTestData(int producerId)
        {
            return new Producer { Id = producerId, FullName = $"Test Producer {producerId}", ProfilePictureURL = $"Test Profile Picture {producerId}", Bio = $"Test Biography {producerId}" };
        }
    }
}