using Microsoft.VisualStudio.TestTools.UnitTesting;
using eTickets.Models;
using Moq;
using eTickets.Data.Interfaces;

namespace eTickets.Data.Services.Tests
{
    [TestClass()]
    public class ActorsServiceTests
    {
        private Mock<IActorRepository> _mockActorRepository;
        private Mock<IUnitOfWork> _mockUnitOfWork;
        private IActorsService _actorsService;

        [TestInitialize]
        public void TestInitialize()
        {
            _mockActorRepository = new Mock<IActorRepository>();
            _mockUnitOfWork = new Mock<IUnitOfWork>();
            _mockUnitOfWork.Setup(u => u.Actors).Returns(_mockActorRepository.Object);

            // initialize ActorsService with mocks
            _actorsService = new ActorsService(_mockUnitOfWork.Object);
        }

        [TestMethod]
        [DataTestMethod]
        [DataRow(1)]
        [DataRow(2)]
        public async Task Test_AddActor_ShouldAddActorToRepository(int actorId)
        {
            // Arrange
            var actor = ActorTemplateForTestData(actorId);

            // Act
            await _actorsService.AddActor(actor);

            // Assert
            _mockUnitOfWork.Verify(u => u.Actors.AddAsync(It.Is<Actor>(a => a.Id == actor.Id)), Times.Once);
            _mockUnitOfWork.Verify(u => u.CommitAsync(), Times.Once);
        }

        [TestMethod]
        [DataTestMethod]
        [DataRow(1)]
        [DataRow(2)]
        [DataRow(3)]
        public async Task Test_GetActorById_ReturnsActorWithMatchingIdAsync(int actorId)
        {
            // Arrange
            var actor = ActorTemplateForTestData(actorId);
            _mockActorRepository.Setup(r => r.GetByIdAsync(actorId)).ReturnsAsync(actor);
            _mockUnitOfWork.Setup(u => u.Actors).Returns(_mockActorRepository.Object);

            // Act
            var result = await _actorsService.GetActorById(actorId);

            // Assert
            Assert.IsNotNull(result);
            Assert.AreEqual(actor.Id, result.Id);
            Assert.AreEqual(actor.FullName, result.FullName);
            Assert.AreEqual(actor.Bio, result.Bio);
            Assert.AreEqual(actor.ProfilePictureURL, result.ProfilePictureURL);
        }

        [TestMethod]
        public async Task Test_GetAllActors_ShouldReturnAllActors()
        {
            // Arrange
            var expectedActors = InitNewActors();
            _mockUnitOfWork.Setup(u => u.Actors.GetAllAsync()).ReturnsAsync(expectedActors);

            // Act
            var actualActors = await _actorsService.GetAllActors();

            // Assert
            Assert.AreEqual(expectedActors.Count, actualActors.ToList().Count);
            Assert.AreEqual(expectedActors[0].Id, actualActors.ToList()[0].Id);
            Assert.AreEqual(expectedActors[1].Id, actualActors.ToList()[1].Id);
        }

        [TestMethod]
        [DataRow(1)]
        [DataRow(2)]
        public async Task Test_DeleteActor_DeletesActorFromRepository(int actorId)
        {
            // Arrange
            _mockActorRepository.Setup(r => r.DeleteAsync(actorId)).Returns(Task.CompletedTask);
            _mockUnitOfWork.Setup(u => u.Actors).Returns(_mockActorRepository.Object);

            // Act
            await _actorsService.DeleteActor(actorId);

            // Assert
            _mockActorRepository.Verify(r => r.DeleteAsync(actorId), Times.Once);
            _mockUnitOfWork.Verify(u => u.CommitAsync(), Times.Once);
        }

        [TestMethod]
        [DataTestMethod]
        [DataRow(1, "Updated Actor Full Name 1", "Test Profile Picture 1", "Updated Bio 1")]
        [DataRow(2, "Updated Actor Full Name 2", "Test Profile Picture 2", "Updated Bio 2")]
        public async Task Test_UpdateActor_ShouldUpdateActorInRepository(int actorId, string updatedFullName, string updateProfile, string updatedBio)
        {
            // Arrange
            var actor = ActorTemplateForTestData(actorId);
            await _actorsService.AddActor(actor);

            // Act
            actor.FullName = updatedFullName;
            actor.Bio = updatedBio;
            actor.ProfilePictureURL= updateProfile;
            await _actorsService.UpdateActor(actorId, actor);

            // Assert
            _mockUnitOfWork.Verify(u => u.Actors.UpdataAsync(actorId, actor), Times.Once);
            _mockUnitOfWork.Verify(u => u.CommitAsync(), Times.AtLeastOnce);
        }

        private List<Actor> InitNewActors()
        {
            var testActors = new List<Actor>
            {
                new Actor { Id = 1, FullName = "Test Actor 1", ProfilePictureURL = "Test Profile Picture 1", Bio = "Test Biography 1" },
                new Actor { Id = 2, FullName = "Test Actor 2", ProfilePictureURL = "Test Profile Picture 2", Bio = "Test Biography 2" }
            };
            return testActors;
        }
        private Actor ActorTemplateForTestData(int actorId)
        {
            return new Actor { Id = actorId, FullName = $"Test Actor {actorId}", ProfilePictureURL = $"Test Profile Picture {actorId}", Bio = $"Test Biography {actorId}" };
        }
    }
}