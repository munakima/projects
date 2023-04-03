using eTickets.Data.Services;
using eTickets.Models;
using Microsoft.AspNetCore.Mvc;

namespace eTickets.Controllers
{
    public class ProducersController : Controller
    {
        private readonly IProducersService _service;

        public ProducersController(IProducersService service)
        {
            _service = service;
        }

        public async Task<IActionResult> Index()
        {
            var data = await _service.GetAllProducers();
            return View(data);
        }

        //Get: Actors/Create()
        public IActionResult Create()
        {
            return View();
        }

        [HttpPost]
        public async Task<IActionResult> Create([Bind("FullName, ProfilePictureURL, Bio")] Producer producer)
        {
            if (!ModelState.IsValid)
            {
                return View(producer);
            }
            await _service.AddProducer(producer);
            //await _service.SaveChange();
            return RedirectToAction(nameof(Index));
        }

        // GET: Actors/Details/1
        [HttpGet]
        public async Task<IActionResult> Details(int id)
        {
            var producerDetails = await _service.GetProducerById(id);

            if (producerDetails == null) return View("NotFound");
            return View(producerDetails);
        }

        //Get: Actors/Edit()
        public async Task<IActionResult> Edit(int id)
        {
            var producerDetails = await _service.GetProducerById(id);
            if (producerDetails == null) return View("NotFound");
            return View(producerDetails);
        }

        [HttpPost]
        public async Task<IActionResult> Edit(int id, [Bind("Id, FullName, ProfilePictureURL, Bio")] Producer producer)
        {
            if (!ModelState.IsValid)
            {
                return View(producer);
            }
            await _service.UpdateProducer(id, producer);
            //await _service.SaveChange();
            return RedirectToAction(nameof(Index));
        }

        // GET: Actors/Delete/1
        [HttpGet]
        public async Task<IActionResult> Delete(int id)
        {
            var producerDetails = await _service.GetProducerById(id);

            if (producerDetails == null) return View("NotFound"); //return NotFound();

            return View(producerDetails);
        }

        [HttpPost, ActionName("Delete")]
        public async Task<IActionResult> DeleteConfirmed(int id)
        {
            var producerInDb = await _service.GetProducerById(id);
            if (producerInDb == null) return View("NotFound"); //return NotFound();

            await _service.DeleteProducer(id);
            //await _service.SaveChange();
            return RedirectToAction(nameof(Index));
        }
    }
}
