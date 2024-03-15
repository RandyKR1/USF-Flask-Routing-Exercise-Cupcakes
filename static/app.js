$('.delete-cupcake').click(deleteCupcake)

async function deleteCupcake() {
    const id = $(this).data('id')
    await axios.delete(`/api/cupcakes/${id}`)
    $(this).parent().remove()
}


$("#new-cupcake-form").on("submit", async function () {
    
  
    let flavor = $("#form-flavor").val();
    let rating = $("#form-rating").val();
    let size = $("#form-size").val();
    let image = $("#form-image").val();
  
    const newCupcakeResponse = await axios.post(`/api/cupcakes`, {
        flavor,
        rating,
        size,
        image
    });
  
    let newCupcake = $(newCupcakeResponse.data.cupcake);
    $("#cup-list").append(newCupcake);
    $("#new-cupcake-form").trigger("reset");
  });