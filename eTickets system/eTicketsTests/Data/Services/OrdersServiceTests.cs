using Microsoft.VisualStudio.TestTools.UnitTesting;
using eTickets.Data.Services;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using eTickets.Data.Interfaces;
using Moq;

namespace eTickets.Data.Services.Tests
{
    [TestClass()]
    public class OrdersServiceTests
    {
        private Mock<IOrderRepository> _mockOrderRepository;
        private Mock<IUnitOfWork> _mockUnitOfWork;
        private IOrdersService _ordersService;

        [TestInitialize]
        public void TestInitialize()
        {
            _mockOrderRepository = new Mock<IOrderRepository>();
            _mockUnitOfWork = new Mock<IUnitOfWork>();
            _mockUnitOfWork.Setup(u => u.Orders).Returns(_mockOrderRepository.Object);

            // initialize ActorsService with mocks
            _ordersService = new OrdersService(_mockUnitOfWork.Object);
        }


    }
}