using eTickets.Models;

namespace eTickets.Data.ViewModels
{
    public class MovieDropdownViewModel
    {
        public List<Producer> Producers { get; set; } = new List<Producer>();
        public List<Cinema> Cinemas { get; set; } = new List<Cinema>();
        public List<Actor> Actors { get; set; } = new List<Actor>();
    }
}
