using Microsoft.VisualStudio.TestTools.UnitTesting;
using eTickets.Data.Services;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using eTickets.Data.Interfaces;
using Moq;
using eTickets.Data.Enums;
using eTickets.Models;
using System.Linq.Expressions;
using eTickets.Data.ViewModels;
using System.Numerics;
using eTickets.Data.Repositories;
using eTickets.Data.Base;
using System.Diagnostics;
using System.Net.Sockets;

namespace eTickets.Data.Services.Tests
{
    [TestClass()]
    public class MoviesServiceTests
    {
        private Mock<IMovieRepository> _mockMovieRepository;
        private Mock<IUnitOfWork> _mockUnitOfWork;
        private IMoviesService _moviesService;

        [TestInitialize]
        public void TestInitialize()
        {
            //_mockMovieRepository = new Mock<IMovieRepository>();
            //_mockUnitOfWork = new Mock<IUnitOfWork>();
            //_mockUnitOfWork.Setup(u => u.Movies).Returns(_mockMovieRepository.Object);

            //// initialize ActorsService with mocks
            //_moviesService = new MoviesService(_mockUnitOfWork.Object);
        }

        [TestMethod]
        public async Task Test_GetAllMovies_ShouldReturnAllMoviesWithCinemas()
        {
            _mockMovieRepository = new Mock<IMovieRepository>();
            _mockUnitOfWork = new Mock<IUnitOfWork>();
            _mockUnitOfWork.Setup(u => u.Movies).Returns(_mockMovieRepository.Object);

            // initialize ActorsService with mocks
            _moviesService = new MoviesService(_mockUnitOfWork.Object);
            // Arrange
            var expectedMovies = new List<Movie>
            {
                new Movie { Id = 1, Name = "Movie 1", Cinema = new Cinema { Id = 1, Name = "Cinema 1" } },
                new Movie { Id = 2, Name = "Movie 2", Cinema = new Cinema { Id = 2, Name = "Cinema 2" } },
                new Movie { Id = 3, Name = "Movie 3", Cinema = new Cinema { Id = 3, Name = "Cinema 3" } }
            };
            _mockMovieRepository.Setup(r => r.GetAllAsync(It.IsAny<Expression<Func<Movie, object>>[]>()))
                .ReturnsAsync(expectedMovies);

            // Act
            var result = await _moviesService.GetAllMovies();

            // Assert
            Assert.IsNotNull(result);
            Assert.AreEqual(expectedMovies.Count, result.Count());
            Assert.IsTrue(expectedMovies.Select(m => m.Id).SequenceEqual(result.Select(m => m.Id)));
            Assert.IsTrue(expectedMovies.Select(m => m.Cinema.Id).SequenceEqual(result.Select(m => m.Cinema.Id)));
        }

        //[TestMethod]
        //public async Task Test_UpdateMovieAsync_ShouldUpdateMovieToDatabase()
        //{
        //    var movieViewModel = new MovieViewModel
        //    {
        //        Id=100,
        //        Name = "Test Movie",
        //        Description = "Test movie description",
        //        Price = 9.99,
        //        ImageUrl = "https://test.com/movie.jpg",
        //        CinemaId = 1,
        //        StartDate = new DateTime(2023, 3, 14),
        //        EndDate = new DateTime(2023, 3, 21),
        //        MovieCategory = MovieCategory.Drama,
        //        ProducerId = 1,
        //        ActorIds = new List<int> { 1, 2, 3 }
        //    };
        //    var newMovie = new Movie()
        //    {
        //        Id = movieViewModel.Id,
        //        Name = movieViewModel.Name,
        //        Description = movieViewModel.Description,
        //        Price = movieViewModel.Price,
        //        ImageURL = movieViewModel.ImageUrl,
        //        StartDate = movieViewModel.StartDate,
        //        EndDate = movieViewModel.EndDate,
        //        CinemaId = movieViewModel.CinemaId,
        //        ProducerId = movieViewModel.ProducerId,
        //        MovieCategory = movieViewModel.MovieCategory,
        //        //Actors_Movies = new List<Actor_Movie>()
        //    };

        //    foreach (var actorId in movieViewModel.ActorIds)
        //    {
        //        newMovie.Actors_Movies.Add(new Actor_Movie
        //        {
        //            MovieId = movieViewModel.Id,
        //            ActorId = actorId
        //        });
                
        //    }

        //    // Act
        //    await _moviesService.AddNewMovieAsync(movieViewModel);
        //    _mockUnitOfWork.Verify(u => u.Movies.AddAsync(newMovie), Times.Once);
        //    _mockUnitOfWork
        //        .Setup(u => u.Actor_Movies.AddAsync(It.IsAny<Actor_Movie>()))
        //        .Verifiable();
        //    // Assert
        //    _mockUnitOfWork.VerifyAll();
        //}
        //[TestMethod]
        //public async Task Test_AddNewMovieAsync_ShouldAddMovieToDatabase()
        //{
        //    var movieViewModel = new MovieViewModel
        //    {
        //        Id = 100,
        //        Name = "Test Movie",
        //        Description = "Test movie description",
        //        Price = 9.99,
        //        ImageUrl = "https://test.com/movie.jpg",
        //        CinemaId = 1,
        //        StartDate = new DateTime(2023, 3, 14),
        //        EndDate = new DateTime(2023, 3, 21),
        //        MovieCategory = MovieCategory.Drama,
        //        ProducerId = 1,
        //        ActorIds = new List<int> { 1, 2, 3 }
        //    };
        //    var newMovie = new Movie()
        //    {
        //        Id = movieViewModel.Id,
        //        Name = movieViewModel.Name,
        //        Description = movieViewModel.Description,
        //        Price = movieViewModel.Price,
        //        ImageURL = movieViewModel.ImageUrl,
        //        StartDate = movieViewModel.StartDate,
        //        EndDate = movieViewModel.EndDate,
        //        CinemaId = movieViewModel.CinemaId,
        //        ProducerId = movieViewModel.ProducerId,
        //        MovieCategory = movieViewModel.MovieCategory,
        //        Actors_Movies = new List<Actor_Movie>()
        //    };
        //    //foreach (var actorId in movieViewModel.ActorIds)
        //    //{
        //    //    newMovie.Actors_Movies.Add(new Actor_Movie
        //    //    {
        //    //        MovieId = movieViewModel.Id,
        //    //        ActorId = actorId
        //    //    });
        //    //}
        //    var newActorMovie = new Actor_Movie();
        //    foreach (var actorId in movieViewModel.ActorIds)
        //    {
        //        newActorMovie = new Actor_Movie()
        //        {
        //            MovieId = newMovie.Id,
        //            ActorId = actorId
        //        };
        //        newMovie.Actors_Movies.Add(newActorMovie);
        //    }
        //    _mockUnitOfWork.Setup(u => u.Movies.AddAsync(newMovie)).Verifiable();
        //    _mockUnitOfWork.Setup(u => u.Actor_Movies.AddAsync(newActorMovie)).Verifiable();
        //    _mockUnitOfWork.Setup(u => u.CommitAsync()).Returns(Task.CompletedTask).Verifiable();

        //    // Act
        //    await _moviesService.AddNewMovieAsync(movieViewModel);

        //    // Assert
        //    _mockUnitOfWork.Verify(u => u.Movies.AddAsync(newMovie), Times.Once);
        //    _mockUnitOfWork.Verify(u => u.Actor_Movies.AddAsync(newActorMovie), Times.Exactly(movieViewModel.ActorIds.Count));
        //    _mockUnitOfWork.Verify(u => u.CommitAsync(), Times.Exactly(2));
        //    // await _moviesService.AddNewMovieAsync(movieViewModel);

        //    //_mockUnitOfWork.Verify(u => u.Movies.AddAsync(newMovie), Times.Once);
        //    ////_mockUnitOfWork.Verify(u => u.Movies.AddAsync(It.Is<Movie>(a => a.Id == movieViewModel.Id)), Times.Once);
        //    //_mockUnitOfWork.Verify(u => u.CommitAsync(), Times.Once);

        //    //_mockUnitOfWork.Verify(u => u.Actor_Movies.AddAsync(newActorMovie), Times.Once);
        //    //_mockUnitOfWork.Verify(u => u.CommitAsync(), Times.Once);
        //}
        //[TestMethod]
        //public async Task Test11()
        //{
        //    // Arrange
        //    var movieViewModel = new MovieViewModel
        //    {
        //        Id = 100,
        //        Name = "Test Movie",
        //        Description = "Test movie description",
        //        Price = 9.99,
        //        ImageUrl = "https://test.com/movie.jpg",
        //        CinemaId = 1,
        //        StartDate = new DateTime(2023, 3, 14),
        //        EndDate = new DateTime(2023, 3, 21),
        //        MovieCategory = MovieCategory.Drama,
        //        ProducerId = 1,
        //        ActorIds = new List<int> { 1, 2, 3 }
        //    };
        //    var unitOfWorkMock = new Mock<IUnitOfWork>();
        //    var moviesRepositoryMock = new Mock<IEntityBaseRepository<Movie>>();
        //    var actorMoviesRepositoryMock = new Mock<IEntityBaseRepository<Act>>();

        //    unitOfWorkMock.Setup(u => u.Movies).Returns(moviesRepositoryMock.Object);
        //    unitOfWorkMock.Setup(u => u.Actor_Movies).Returns(actorMoviesRepositoryMock.Object);

        //    var moviesService = new MoviesService(unitOfWorkMock.Object);

        //    // Act
        //    await moviesService.AddNewMovieAsync(movieViewModel);

        //    // Assert
        //    moviesRepositoryMock.Verify(r => r.AddAsync(It.IsAny<Movie>()), Times.Once);
        //    actorMoviesRepositoryMock.Verify(r => r.AddAsync(It.IsAny<Actor_Movie>()), Times.Exactly(movieViewModel.ActorIds.Count));
        //    unitOfWorkMock.Verify(u => u.CommitAsync(), Times.Exactly(2));
        //}
       
        private List<Movie> InitiMovies()
        {
            var movies = new List<Movie>()
                    {
                        new Movie()
                        {
                            Id= 1,
                            Name = "Movie 1",
                            Description = "This is the Life movie description",
                            Price = 39.50,
                            ImageURL = "http://dotnethow.net/images/movies/movie-3.jpeg",
                            StartDate = DateTime.Now.AddDays(-10),
                            EndDate = DateTime.Now.AddDays(10),
                            CinemaId = 2,
                            ProducerId = 2,
                            MovieCategory = MovieCategory.Documentary
                        },
                        new Movie()
                        {
                            Id= 2,
                            Name = "Movie 2",
                            Description = "This is the Shawshank Redemption description",
                            Price = 29.50,
                            ImageURL = "http://dotnethow.net/images/movies/movie-1.jpeg",
                            StartDate = DateTime.Now,
                            EndDate = DateTime.Now.AddDays(3),
                            CinemaId = 1,
                            ProducerId = 1,
                            MovieCategory = MovieCategory.Action
                        } };
            return movies;
        }
    }
}