using System.ComponentModel.DataAnnotations;

namespace eTickets.Models
{
    public class Order
    {
        [Key]
        public int Id { get; set; }

        [EmailAddress]
        [Display(Name = "Email")]
        [Required(ErrorMessage = "Email is Required")]
        [StringLength(50, MinimumLength = 3, ErrorMessage = "Email must be between 3 and 50 characters")]
        public string Email { get; set; }

        [Display(Name = "User Id")]
        [Required(ErrorMessage = "User Id is Required")]
        [StringLength(50, MinimumLength = 3, ErrorMessage = "User Id must be between 3 and 50 characters")]
        public string UserId { get; set; }

        public List<OrderItem> OrderItems { get; set; }
    }
}
