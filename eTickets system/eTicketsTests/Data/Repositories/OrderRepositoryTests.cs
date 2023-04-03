using Microsoft.VisualStudio.TestTools.UnitTesting;
using Moq;
using eTickets.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.ChangeTracking;
using eTickets.Data.Interfaces;

namespace eTickets.Data.Repositories.Tests
{
    [TestClass()]
    public class OrderRepositoryTests
    {
        private IOrderRepository _orderRepository;
        private Mock<AppDbContext> _mockContext;

        //[TestInitialize]
        //public void Initialize()
        //{
        //    var orders = new List<Order>
        //    {
        //        new Order { Id = 1, UserId = "user1", Email = "test1@test.com" },
        //        new Order { Id = 2, UserId = "user1", Email = "test2@test.com" }
        //    };

        //    var mockOrders = new Mock<DbSet<Order>>();
        //    mockOrders.As<IAsyncEnumerable<Order>>()
        //              .Setup(m => m.GetAsyncEnumerator(It.IsAny<CancellationToken>()))
        //              .Returns(new TestAsyncEnumerator<Order>(orders.GetEnumerator()));

        //    mockOrders.As<IQueryable<Order>>()
        //              .Setup(m => m.Provider)
        //              .Returns(new TestAsyncQueryProvider<Order>(orders.AsQueryable().Provider));

        //    mockOrders.As<IQueryable<Order>>().Setup(m => m.Expression).Returns(orders.AsQueryable().Expression);
        //    mockOrders.As<IQueryable<Order>>().Setup(m => m.ElementType).Returns(orders.AsQueryable().ElementType);
        //    mockOrders.As<IQueryable<Order>>().Setup(m => m.GetEnumerator()).Returns(orders.AsQueryable().GetEnumerator());

        //    _mockContext = new Mock<AppDbContext>();
        //    _mockContext.Setup(c => c.Orders).Returns(mockOrders.Object);

        //    _orderRepository = new OrderRepository(_mockContext.Object);
        //}
        //[TestMethod]
        //public async Task GetOrdersByUserIDAsync_ReturnsOrders()
        //{
        //    string userId = "user1";
        //    // arrange
        //    var expectedOrders = new List<Order>
        //    {
        //        new Order { Id = 1, UserId = "user1", Email = "test1@test.com" },
        //        new Order { Id = 2, UserId = "user1", Email = "test2@test.com" }
        //    };

        //    var queryableOrders = expectedOrders.AsQueryable();
        //    var mockSet = new Mock<DbSet<Order>>();
            

        //    _mockContext.Setup(c => c.Orders).Returns(_mockContext.Object.CreateMockOrdersDbSet);

        //    // act
        //    var actualOrders = await _orderRepository.GetOrdersByUserIDAsync("user1");

        //    // assert
        //    Assert.IsNotNull(actualOrders);
        //    Assert.AreEqual(expectedOrders.Count, actualOrders.Count);
        //    Assert.AreEqual(expectedOrders[0].UserId, actualOrders[0].UserId);
        //    Assert.AreEqual(expectedOrders[0].Email, actualOrders[0].Email);
        //    Assert.AreEqual(expectedOrders[1].UserId, actualOrders[1].UserId);
        //    Assert.AreEqual(expectedOrders[1].Email, actualOrders[1].Email);
        //}
        //public void Initialize()
        //{
        //    _mockContext = new Mock<AppDbContext>();
        //    //_mockContext.Setup(s => s.Orders.GetAsyncEnumerator(CancellationToken.None)).Returns(GetTestValues);
        //    _mockContext.Setup(s => s.Orders).Returns(_mockContext.Object.CreateMockOrdersDbSet);
        //    _repository = new OrderRepository(_mockContext.Object);
        //}
        //public void Initialize()
        //{
        //    //var orders = new List<Order>();
        //    //var mockSet = new Mock<DbSet<Order>>();
        //    //mockSet.As<IQueryable<Order>>().Setup(m => m.Provider).Returns(orders.AsQueryable().Provider);
        //    //mockSet.As<IQueryable<Order>>().Setup(m => m.Expression).Returns(orders.AsQueryable().Expression);
        //    //mockSet.As<IQueryable<Order>>().Setup(m => m.ElementType).Returns(orders.AsQueryable().ElementType);
        //    //mockSet.As<IQueryable<Order>>().Setup(m => m.GetEnumerator()).Returns(() => orders.GetEnumerator());

        //    _mockContext = new Mock<AppDbContext>();
        //    //2
        //    //_mockContext.Setup(c => c.Orders).Returns(mockSet.Object);
        //    _mockContext.Setup(c => c.CreateMockOrdersDbSet()).Returns(() => new Mock<DbSet<Order>>().Object);
        //    _mockContext.Setup(c => c.Orders).Returns(() => _mockContext.Object.CreateMockOrdersDbSet());
        //    _repository = new OrderRepository(_mockContext.Object);
        //}
        //public void Initialize()
        //{
        //    var orders = new List<Order>();
        //    var mockSet = new Mock<DbSet<Order>>();
        //    mockSet.As<IQueryable<Order>>().Setup(m => m.Provider).Returns(orders.AsQueryable().Provider);
        //    mockSet.As<IQueryable<Order>>().Setup(m => m.Expression).Returns(orders.AsQueryable().Expression);
        //    mockSet.As<IQueryable<Order>>().Setup(m => m.ElementType).Returns(orders.AsQueryable().ElementType);
        //    mockSet.As<IQueryable<Order>>().Setup(m => m.GetEnumerator()).Returns(() => orders.GetEnumerator());

        //    _mockContext = new Mock<AppDbContext>();
        //    //2
        //    _mockContext.Setup(c => c.Orders).Returns(mockSet.Object);
        //    _repository = new OrderRepository(_mockContext.Object);
        //}
        public static async IAsyncEnumerable<Order> GetTestValues()
        {
            yield return new Order { Id = 1, UserId = "user1", Email = "test1@test.com" };
            // yield return "bar";

            await Task.CompletedTask; // to make the compiler warning go away
        }

        //[TestMethod]
        //public async Task GetOrdersByUserIDAsync_ReturnsOrders()
        //{
        //    string userId = "user1";
        //    // arrange
        //    var expectedOrders = new List<Order>
        //    {
        //    new Order { Id = 1, UserId = "user1", Email = "test1@test.com" },
        //    new Order { Id = 2, UserId = "user1", Email = "test2@test.com" }
        //     };
        //    var expectedOrder = new Order { Id = 1, UserId = "user1", Email = "test1@test.com" };
           

        //    var result = await _orderRepository.GetOrdersByUserIDAsync(userId);
        //    Assert.AreEqual(expectedOrders[0].UserId, result[0].UserId);
        //    Assert.AreEqual(expectedOrders[0].Email, result[0].Email);

        //    //// act
        //    //Assert.AreEqual(expectedOrders[0].UserId, result[0].UserId);
        //    //Assert.AreEqual(expectedOrders[0].Email, result[0].Email);
        //    //Assert.AreEqual(expectedOrders[1].UserId, result[1].UserId);
        //    //Assert.AreEqual(expectedOrders[1].Email, result[1].Email);
        //}
        //[TestMethod]
        //public async Task GetOrdersByUserIDAsync_ReturnsOrders()
        //{
        //    string userId = "user1";
        //    // arrange
        //    var expectedOrders = new List<Order>
        //    {
        //    new Order { Id = 1, UserId = "user1", Email = "test1@test.com" },
        //    new Order { Id = 2, UserId = "user1", Email = "test2@test.com" }
        //     };

        //    _mockContext.Setup(c => c.Orders
        //        .Include(n => n.OrderItems)
        //        .ThenInclude(n => n.Movie)
        //        .Where(n => n.UserId == userId).ToListAsync(CancellationToken.None))
        //        .ReturnsAsync(expectedOrders);

        //    // act
        //    var actualOrders = await _repository.GetOrdersByUserIDAsync("user1");

        //    // assert
        //    Assert.IsNotNull(actualOrders);
        //    Assert.AreEqual(expectedOrders.Count, actualOrders.Count);
        //    //Assert.AreEqual(expectedOrders[0].UserId, actualOrders[0].UserId);
        //    //Assert.AreEqual(expectedOrders[0].Email, actualOrders[0].Email);
        //    //Assert.AreEqual(expectedOrders[1].UserId, actualOrders[1].UserId);
        //    //Assert.AreEqual(expectedOrders[1].Email, actualOrders[1].Email);
        //    Assert.AreEqual(expectedOrders, actualOrders.ToList());
        //}


        //[TestMethod]
        //public async Task AddOrderAsync_AddsOrder()
        //{
        //    // arrange
        //    var userId = "test_user_id";
        //    var email = "test_email";
        //    var expectedOrder = new Order { UserId = userId, Email = email };

        //    _mockContext.Setup(c => c.Orders.AddAsync(It.IsAny<Order>(), CancellationToken.None))
        //        .Callback<Order, CancellationToken>((order, _) => { order.Id = expectedOrder.Id; })
        //        .Returns(new ValueTask<EntityEntry<Order>>(Task.FromResult(new EntityEntry<Order>(default))));

        //    // act
        //    var result = await _repository.AddOrderAsync(userId, email);

        //    // assert
        //    Assert.AreEqual(expectedOrder.UserId, result.UserId);
        //    Assert.AreEqual(expectedOrder.Email, result.Email);
        //    Assert.IsNotNull(result.Id);
        //}


        //[TestMethod]
        //public async Task AddOrderAsync_AddsOrder()
        //{
        //    // arrange
        //    var userId = "test_user_id";
        //    var email = "test_email";
        //    var expectedOrder = new Order { UserId = userId, Email = email };

        //    _mockContext.Setup(c => c.Orders.AddAsync(It.IsAny<Order>(), CancellationToken.None))
        //        .Callback<Order, CancellationToken>((order, _) => { order.Id = expectedOrder.Id; })
        //        .Returns(new ValueTask<EntityEntry<Order>>(Task.FromResult(new EntityEntry<Order>(default))));

        //    // act
        //    var result = await _repository.AddOrderAsync(userId, email);

        //    // assert
        //    Assert.AreEqual(expectedOrder.UserId, result.UserId);
        //    Assert.AreEqual(expectedOrder.Email, result.Email);
        //    Assert.IsNotNull(result.Id);
        //}
    }
}