using eTickets.Data.Services;
using eTickets.Models;
using Microsoft.AspNetCore.Mvc;

namespace eTickets.Controllers
{
    public class CinemasController : Controller
    {
        private readonly ICinemasService _service;

        public CinemasController(ICinemasService service)
        {
            _service = service;
        }

        public async Task<IActionResult> Index()
        {
            var data = await _service.GetAllCinemas();
            return View(data);
        }

        //Get: Cinemas/Create()
        public IActionResult Create()
        {
            return View();
        }

        [HttpPost]
        public async Task<IActionResult> Create([Bind("Logo, Name, Description")] Cinema cinema)
        {
            if (!ModelState.IsValid)
            {
                return View(cinema);
            }
            await _service.AddCinema(cinema);
            return RedirectToAction(nameof(Index));
        }

        // GET: Cinemas/Details/1
        [HttpGet]
        public async Task<IActionResult> Details(int id)
        {
            var cinema = await _service.GetCinemaById(id);

            if (cinema == null) return View("NotFound");
            return View(cinema);
        }

        //Get: Cinemas/Edit()
        public async Task<IActionResult> Edit(int id)
        {
            var cinema = await _service.GetCinemaById(id);
            if (cinema == null) return View("NotFound");
            return View(cinema);
        }

        [HttpPost]
        public async Task<IActionResult> Edit(int id, [Bind("Id, Logo, Name, Description")] Cinema cinema)
        {
            if (!ModelState.IsValid)
            {
                return View(cinema);
            }
            await _service.UpdateCinema(id, cinema);
            return RedirectToAction(nameof(Index));
        }

        // GET: Actors/Delete/1
        [HttpGet]
        public async Task<IActionResult> Delete(int id)
        {
            var cinema = await _service.GetCinemaById(id);

            if (cinema == null) return View("NotFound");

            return View(cinema);
        }

        [HttpPost, ActionName("Delete")]
        public async Task<IActionResult> DeleteConfirmed(int id)
        {
            var cinemaDB = await _service.GetCinemaById(id);
            if (cinemaDB == null) return View("NotFound");

            await _service.DeleteCinema(id);
            return RedirectToAction(nameof(Index));
        }
    }
}
