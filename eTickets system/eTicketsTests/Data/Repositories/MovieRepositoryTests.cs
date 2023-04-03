using Microsoft.VisualStudio.TestTools.UnitTesting;
using eTickets.Data.Interfaces;
using Microsoft.EntityFrameworkCore;
using eTickets.Models;
using eTickets.Data.Enums;
using eTickets.Data.ViewModels;

namespace eTickets.Data.Repositories.Tests
{
    [TestClass()]
    public class MovieRepositoryTests
    {
        private IMovieRepository _movieRepository;
        private DbContextOptions<AppDbContext> _options;
        private static AppDbContext _context;

        [TestInitialize]
        public void TestInitialize()
        {
            _options = new DbContextOptionsBuilder<AppDbContext>()
                .UseInMemoryDatabase(databaseName: "TestDb")
                .Options;

            _context = new AppDbContext(_options);
            _context.Movies.AddRangeAsync(InitiMovies());
            _context.Cinemas.AddRangeAsync(InitiCinemas());
            _context.Producers.AddRangeAsync(InitiProducers());
            _context.Actors.AddRangeAsync(InitiActors());
            _context.Actors_Movies.AddRangeAsync(InitiActorMovies());

            _context.SaveChangesAsync().Wait();
            _movieRepository = new MovieRepository(_context);
        }
        [ClassCleanup]
        public static void MyClassCleanup()
        {
            // This code runs only once after all test methods
            _context.Database.EnsureDeleted();
            _context.Dispose();
        }

        [TestMethod]
        public async Task Test_GetNewMovieDropdownsValues_ReturnsExpectedValues()
        {
            var result = await _movieRepository.GetNewMovieDropdownsValues();

            // Assert
            Assert.AreEqual(2, result.Actors.Count);
            Assert.AreEqual(1, result.Actors[0].Id);
            Assert.AreEqual("Actor 1", result.Actors[0].FullName);
            Assert.AreEqual(2, result.Actors[1].Id);
            Assert.AreEqual("Actor 2", result.Actors[1].FullName);

            Assert.AreEqual(2, result.Cinemas.Count);
            Assert.AreEqual(1, result.Cinemas[0].Id);
            Assert.AreEqual("Cinema 1", result.Cinemas[0].Name);
            Assert.AreEqual(2, result.Cinemas[1].Id);
            Assert.AreEqual("Cinema 2", result.Cinemas[1].Name);

            Assert.AreEqual(2, result.Producers.Count);
            Assert.AreEqual(1, result.Producers[0].Id);
            Assert.AreEqual("Producer 1", result.Producers[0].FullName);
            Assert.AreEqual(2, result.Producers[1].Id);
            Assert.AreEqual("Producer 2", result.Producers[1].FullName);
            MyClassCleanup();
        }
        [TestMethod]
        public async Task Test_GetMovieDetailsAsync_ShouldReturnMovieDetails()
        {
            int id = 1;

            var result = await _movieRepository.GetMovieInfo(id);
            var movie = new Movie()
            {
                Id = 1,
                Name = "Movie 1",
                Description = "This is the Life movie description",
                Price = 39.50,
                ImageURL = "http://dotnethow.net/images/movies/movie-3.jpeg",
                StartDate = DateTime.Now.AddDays(-10),
                EndDate = DateTime.Now.AddDays(10),
                CinemaId = 2,
                ProducerId = 2,
                MovieCategory = MovieCategory.Documentary
            };
            // Assert
            Assert.IsNotNull(result);
            Assert.AreEqual(movie.Id, result.Id);
            Assert.AreEqual(movie.Name, result.Name);
            Assert.AreEqual("Cinema 2", result.Cinema.Name);
            Assert.AreEqual("Producer 2", result.Producer.FullName);
            Assert.AreEqual(2, result.Actors_Movies.Count);
            Assert.AreEqual("Actor 1", result.Actors_Movies.First().Actor.FullName);
            MyClassCleanup();

        }
        [TestMethod]
        public async Task Test_UpdateMovieAsync_ShouldUpdateMovieAndActors()
        {
            var newMovie = new MovieViewModel()
            {
                Id = 1,
                Name = "Updated Movie 1",
                Description = "This is the updated Life movie description",
                Price = 49.50,
                ImageUrl = "http://dotnethow.net/images/movies/movie-3-updated.jpeg",
                StartDate = DateTime.Now.AddDays(-5),
                EndDate = DateTime.Now.AddDays(5),
                CinemaId = 1,
                ProducerId = 1,
                MovieCategory = MovieCategory.Action,
                ActorIds = new List<int> { 1, 2 }
            };
            await _movieRepository.UpdateMovieAsync(newMovie);
            var result = await _movieRepository.GetMovieInfo(newMovie.Id);

            // Assert
            Assert.AreEqual(newMovie.Name, result.Name);
            Assert.AreEqual(newMovie.Description, result.Description);
            Assert.AreEqual(newMovie.Price, result.Price);
            Assert.AreEqual(newMovie.ImageUrl, result.ImageURL);
            Assert.AreEqual(newMovie.StartDate, result.StartDate);
            Assert.AreEqual(newMovie.EndDate, result.EndDate);
            Assert.AreEqual(newMovie.CinemaId, result.CinemaId);
            Assert.AreEqual(newMovie.ProducerId, result.ProducerId);
            Assert.AreEqual(newMovie.MovieCategory, result.MovieCategory);
            Assert.AreEqual(newMovie.ActorIds.Count, result.Actors_Movies.Count);
            Assert.IsTrue(result.Actors_Movies.All(a => newMovie.ActorIds.Contains(a.ActorId)));
            MyClassCleanup();

        }
        [TestMethod]
        public async Task Test_AddNewMovieAsync_ShouldUpdateMovieAndActors()
        {
            var movieViewModel = new MovieViewModel()
            {
                Id = 100,
                Name = "new Movie 1",
                Description = "This is the updated Life movie description",
                Price = 49.50,
                ImageUrl = "http://dotnethow.net/images/movies/movie-3-updated.jpeg",
                StartDate = DateTime.Now.AddDays(-5),
                EndDate = DateTime.Now.AddDays(5),
                CinemaId = 1,
                ProducerId = 1,
                MovieCategory = MovieCategory.Action,
                ActorIds = new List<int> { 1, 2 }
            };
            var newMovie = new Movie()
            {
                Id = movieViewModel.Id,
                Name = movieViewModel.Name,
                Description = movieViewModel.Description,
                Price = movieViewModel.Price,
                ImageURL = movieViewModel.ImageUrl,
                StartDate = movieViewModel.StartDate,
                EndDate = movieViewModel.EndDate,
                CinemaId = movieViewModel.CinemaId,
                ProducerId = movieViewModel.ProducerId,
                MovieCategory = movieViewModel.MovieCategory,
                Actors_Movies = new List<Actor_Movie>()
            };

            foreach (var actorId in movieViewModel.ActorIds)
            {
                newMovie.Actors_Movies.Add(new Actor_Movie
                {
                    MovieId = movieViewModel.Id,
                    ActorId = actorId
                });

            }
            await _movieRepository.AddNewMovieAsync(movieViewModel);
            var result = await _movieRepository.GetMovieInfo(newMovie.Id);

            // Assert
            Assert.AreEqual(newMovie.Description, result.Description);
            Assert.AreEqual(newMovie.Price, result.Price);
            Assert.AreEqual(newMovie.ImageURL, result.ImageURL);
            Assert.AreEqual(newMovie.StartDate, result.StartDate);
            Assert.AreEqual(newMovie.EndDate, result.EndDate);
            Assert.AreEqual(newMovie.CinemaId, result.CinemaId);
            Assert.AreEqual(newMovie.ProducerId, result.ProducerId);
            Assert.AreEqual(newMovie.MovieCategory, result.MovieCategory);
            Assert.AreEqual(newMovie.Actors_Movies.Count, result.Actors_Movies.Count);
            Assert.AreEqual(newMovie.Actors_Movies,result.Actors_Movies.First().Actor.FullName);
            MyClassCleanup();
        }

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
        private List<Producer> InitiProducers()
        {
            var producers = new List<Producer>()
                    {
                        new Producer()
                        {
                            Id=1,
                            FullName = "Producer 1",
                            Bio = "This is the Bio of the first actor",
                            ProfilePictureURL = "http://dotnethow.net/images/producers/producer-1.jpeg"

                        },
                        new Producer()
                        {
                            Id=2,
                            FullName = "Producer 2",
                            Bio = "This is the Bio of the second actor",
                            ProfilePictureURL = "http://dotnethow.net/images/producers/producer-2.jpeg"
                        } };
            return producers;
        }
        private List<Cinema> InitiCinemas()
        {
            var cinemas = new List<Cinema>()
                    {
                        new Cinema()
                        {
                            Id=1,
                            Name = "Cinema 1",
                            Logo = "http://dotnethow.net/images/cinemas/cinema-1.jpeg",
                            Description = "This is the description of the first cinema"
                        },
                        new Cinema()
                        {
                            Id=2,
                            Name = "Cinema 2",
                            Logo = "http://dotnethow.net/images/cinemas/cinema-2.jpeg",
                            Description = "This is the description of the first cinema"
                        } };
            return cinemas;
        }
        private List<Actor_Movie> InitiActorMovies()
        {
            var actor_Movies = new List<Actor_Movie>()
                    {
                       new Actor_Movie()
                        {
                            ActorId = 1,
                            MovieId = 1
                        },
                        new Actor_Movie()
                        {
                            ActorId = 3,
                            MovieId = 1
                        } };
            return actor_Movies;
        }
        private List<Actor> InitiActors()
        {
            var actors = new List<Actor>()
                    {
                        new Actor()
                        {
                            Id=1,
                            FullName = "Actor 1",
                            Bio = "This is the Bio of the first actor",
                            ProfilePictureURL = "http://dotnethow.net/images/actors/actor-1.jpeg"

                        },
                        new Actor()
                        {
                            Id=2,
                            FullName = "Actor 2",
                            Bio = "This is the Bio of the second actor",
                            ProfilePictureURL = "http://dotnethow.net/images/actors/actor-2.jpeg"
                        } };
            return actors;
        }

    }
}