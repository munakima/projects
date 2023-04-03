using System.ComponentModel.DataAnnotations;

namespace eTickets.Models
{
    public class ShoppingCartItem
    {
        [Key]
        public int Id { get; set; }

        public Movie Movie { get; set; }

        [Display(Name = "Quantity")]
        [Required(ErrorMessage = "Quantity is Required")]
        [Range(0, 100000)]
        public int Qauntity { get; set; }

        [MaxLength(100)]
        public string ShoppingCartId { get; set; }
    }
}
