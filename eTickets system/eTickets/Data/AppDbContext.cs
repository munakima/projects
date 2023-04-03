using eTickets.Models;
using Microsoft.EntityFrameworkCore;
using Moq;

namespace eTickets.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext() : base()
        {
        }
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        {

        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Actor_Movie>().HasKey(am => new
            {
                am.ActorId,
                am.MovieId
            });

            modelBuilder.Entity<Actor_Movie>().HasOne(am => am.Actor).WithMany(a => a.Actors_Movies).HasForeignKey(am => am.ActorId);
            modelBuilder.Entity<Actor_Movie>().HasOne(am => am.Movie).WithMany(m => m.Actors_Movies).HasForeignKey(am => am.MovieId);

            base.OnModelCreating(modelBuilder);
        }

        //// Factory method to create a mock DbSet<Order>
        //public virtual DbSet<Order> CreateMockOrdersDbSet()
        //{
        //    var orders = new List<Order>();
        //    var mockSet = new Mock<DbSet<Order>>();
        //    mockSet.As<IQueryable<Order>>().Setup(m => m.Provider).Returns(orders.AsQueryable().Provider);
        //    mockSet.As<IQueryable<Order>>().Setup(m => m.Expression).Returns(orders.AsQueryable().Expression);
        //    mockSet.As<IQueryable<Order>>().Setup(m => m.ElementType).Returns(orders.AsQueryable().ElementType);
        //    mockSet.As<IQueryable<Order>>().Setup(m => m.GetEnumerator()).Returns(() => orders.GetEnumerator());
        //    return mockSet.Object;
        //}

        public virtual DbSet<Cinema> Cinemas { get; set; }
        public virtual DbSet<Actor_Movie> Actors_Movies { get; set; }
        public virtual DbSet<Movie> Movies { get; set; }
        public virtual DbSet<Producer> Producers { get; set; }
        public virtual DbSet<Actor> Actors { get; set; }

        //Orders related tables
        public virtual DbSet<Order> Orders { get; set; }
        public virtual DbSet<OrderItem> OrderItems { get; set; }

        public virtual DbSet<ShoppingCartItem> ShoppingCartItems { get; set; }
    }
}
