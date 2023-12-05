/*=============== SHOW HIDDEN - PASSWORD ===============*/
const showHiddenPass = (inputPass, inputIcon) =>{
    const input = document.getElementById(inputPass),
          iconEye = document.getElementById(inputIcon)
          
    iconEye.addEventListener('click', () =>{
        // Change password to text
        if(input.type === 'password'){
            // Switch to text
            input.type = 'text'
 
            // Add icon
            iconEye.classList.add('ri-eye-line')
            // Remove icon
            iconEye.classList.remove('ri-eye-off-line')
        }else{
            // Change to password
            input.type = 'password'
 
            // Remove icon
            iconEye.classList.remove('ri-eye-line')
            // Add icon
            iconEye.classList.add('ri-eye-off-line')
        }
    })
 }
 
 showHiddenPass('input-pass','input-icon')


/*=============== SHOW RECIPE IN GRID ===============*/


 document.addEventListener('DOMContentLoaded', function () {
    const recipeBoxes = document.querySelectorAll('.recipe-box');

    recipeBoxes.forEach(box => {
        box.addEventListener('click', function () {
            // Toggle the 'active' class to expand/collapse the ingredients list
            this.classList.toggle('active');
        });
    });
});


