using Microsoft.VisualStudio.TestTools.UnitTesting;
using eTickets.Data.Interfaces;
using Moq;
using eTickets.Models;

namespace eTickets.Data.Services.Tests
{
    [TestClass()]
    public class CinemasServiceTests
    {
        private Mock<ICinemaRepository> _mockCinemaRepository;
        private Mock<IUnitOfWork> _mockUnitOfWork;
        private ICinemasService _cinemasService;

        [TestInitialize]
        public void TestInitialize()
        {
            _mockCinemaRepository = new Mock<ICinemaRepository>();
            _mockUnitOfWork = new Mock<IUnitOfWork>();
            _mockUnitOfWork.Setup(u => u.Cinemas).Returns(_mockCinemaRepository.Object);

            // initialize CinemasService with mocks
            _cinemasService = new CinemasService(_mockUnitOfWork.Object);
        }

        [TestMethod]
        [DataTestMethod]
        [DataRow(1)]
        [DataRow(2)]
        public async Task Test_AddCinema_ShouldAddCinemaToRepository(int cinemaId)
        {
            // Arrange
            var cinema = CinemaTemplateForTestData(cinemaId);

            // Act
            await _cinemasService.AddCinema(cinema);

            // Assert
            _mockUnitOfWork.Verify(u => u.Cinemas.AddAsync(It.Is<Cinema>(a => a.Id == cinema.Id)), Times.Once);
            _mockUnitOfWork.Verify(u => u.CommitAsync(), Times.Once);
        }

        [TestMethod]
        [DataTestMethod]
        [DataRow(1)]
        [DataRow(2)]
        [DataRow(3)]
        public async Task Test_GetCinemaById_ReturnsActorWithMatchingIdAsync(int cinemaId)
        {
            // Arrange
            var cinema = CinemaTemplateForTestData(cinemaId);
            _mockCinemaRepository.Setup(r => r.GetByIdAsync(cinemaId)).ReturnsAsync(cinema);
            _mockUnitOfWork.Setup(u => u.Cinemas).Returns(_mockCinemaRepository.Object);

            // Act
            var result = await _cinemasService.GetCinemaById(cinemaId);

            // Assert
            Assert.IsNotNull(result);
            Assert.AreEqual(cinema.Id, result.Id);
            Assert.AreEqual(cinema.Name, result.Name);
            Assert.AreEqual(cinema.Logo, result.Logo);
            Assert.AreEqual(cinema.Description, result.Description);

        }

        [TestMethod]
        public async Task Test_GetAllCinemas_ShouldReturnAllCinemas()
        {
            // Arrange
            var expectedCinemas = InitNewCinemas();
            _mockUnitOfWork.Setup(u => u.Cinemas.GetAllAsync()).ReturnsAsync(expectedCinemas);

            // Act
            var actualCinemas = await _cinemasService.GetAllCinemas();

            // Assert
            Assert.AreEqual(expectedCinemas.Count, actualCinemas.ToList().Count);
            Assert.AreEqual(expectedCinemas[0].Id, actualCinemas.ToList()[0].Id);
            Assert.AreEqual(expectedCinemas[1].Id, actualCinemas.ToList()[1].Id);
        }

        [TestMethod]
        [DataRow(1)]
        [DataRow(2)]
        public async Task Test_DeleteCinema_DeletesCinemaFromRepository(int cinemaId)
        {
            // Arrange
            _mockCinemaRepository.Setup(r => r.DeleteAsync(cinemaId)).Returns(Task.CompletedTask);
            _mockUnitOfWork.Setup(u => u.Cinemas).Returns(_mockCinemaRepository.Object);

            // Act
            await _cinemasService.DeleteCinema(cinemaId);

            // Assert
            _mockCinemaRepository.Verify(r => r.DeleteAsync(cinemaId), Times.Once);
            _mockUnitOfWork.Verify(u => u.CommitAsync(), Times.Once);
        }

        [TestMethod]
        [DataTestMethod]
        [DataRow(1, "Updated Name 1", "Test Logo 1", "Updated Description 1")]
        [DataRow(2, "Updated Name 2", "Test Logo 2", "Updated Description 2")]
        public async Task Test_UpdateCinema_ShouldUpdateCinemaInRepository(int cinemaId, string updatedName, string updatedLogo, string updatedDescription)
        {
            // Arrange
            var cinema = CinemaTemplateForTestData(cinemaId);
            await _cinemasService.AddCinema(cinema);

            // Act
            cinema.Name = updatedName;
            cinema.Logo = updatedLogo;
            cinema.Description = updatedDescription;
            await _cinemasService.UpdateCinema(cinemaId, cinema);

            // Assert
            _mockUnitOfWork.Verify(u => u.Cinemas.UpdataAsync(cinemaId, cinema), Times.Once);
            _mockUnitOfWork.Verify(u => u.CommitAsync(), Times.AtLeastOnce);
        }

        private List<Cinema> InitNewCinemas()
        {
            var testCinemas = new List<Cinema>
            {
                new Cinema { Id = 1, Name = "Test Cinema 1", Logo = "Test Logo 1", Description = "Test Description 1" },
                new Cinema { Id = 2, Name = "Test Cinema 2", Logo = "Test Logo 2", Description = "Test Description 2" }
            };
            return testCinemas;
        }
        private Cinema CinemaTemplateForTestData(int cinemaId)
        {
            return new Cinema { Id = cinemaId, Name = $"Test Cinema {cinemaId}", Logo = $"Test Logo {cinemaId}", Description = $"Test Description {cinemaId}" };
        }
    }
}