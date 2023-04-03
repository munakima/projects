using eTickets.Data.Base;
using eTickets.Data.Enums;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace eTickets.Models
{
    public class Movie : IEntityBase
    {
        [Key]
        public int Id { get; set; }

        [Display(Name = "Name")]
        [Required(ErrorMessage = "Movie Name is required")]
        public string Name { get; set; }

        [Display(Name = "Description")]
        [Required(ErrorMessage = "Description is Required")]
        [StringLength(255, MinimumLength = 3, ErrorMessage = "Description must be between 3 and 255 characters")]
        public string Description { get; set; }

        [Display(Name = "Start Date")]
        public DateTime StartDate { get; set; }

        [Display(Name = "End Date")]
        public DateTime EndDate { get; set; }

        [Display(Name = "Price")]
        public double Price { get; set; }

        [Display(Name = "Movie Category")]
        [Required(ErrorMessage = "Movie category is Required")]
        public MovieCategory MovieCategory { get; set; }

        [Display(Name = "ImageUrl")]
        [Required(ErrorMessage = "ImageUrl is Required")]
        public string ImageURL { get; set; }

        //Relationships
        public List<Actor_Movie>? Actors_Movies { get; set; }

        //Cinema
        public int CinemaId { get; set; }
        [ForeignKey(nameof(CinemaId))] //[ForeignKey("CinemaId")]
        public Cinema Cinema { get; set; }

        //Producer
        public int ProducerId { get; set; }
        [ForeignKey(nameof(ProducerId))] //[ForeignKey("ProducerId")]
        public Producer Producer { get; set; }
    }
}
