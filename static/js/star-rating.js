// document.addEventListener("DOMContentLoaded", function() {
//     const stars = document.querySelectorAll(".star-rating label");
//
//     stars.forEach((star, index) => {
//         star.addEventListener("mouseenter", function() {
//             for (let i = 0; i <= index; i++) {
//                 stars[i].classList.add("glow");
//             }
//         });
//
//         star.addEventListener("mouseleave", function() {
//             stars.forEach(star => {
//                 star.classList.remove("glow");
//             });
//         });
//
//         star.addEventListener("click", function() {
//             const rating = index + 1;
//             console.log(rating)
//             document.querySelector("input[name='rating']").value = rating;
//             for (let i = 0; i <= index; i++) {
//                 stars[i].classList.add("glow");
//             }
//         });
//     });
// });

document.addEventListener("DOMContentLoaded", function() {
    const stars = document.querySelectorAll(".star-rating label");

    let selectedRating = 0; // 保存当前选择的评分值

    stars.forEach((star, index) => {
        star.addEventListener("mouseenter", function() {
            if (selectedRating === 0) {
                for (let i = 0; i <= index; i++) {
                    stars[i].classList.add("glow");
                }
            }
        });

        star.addEventListener("mouseleave", function() {
            if (selectedRating === 0) {
                stars.forEach(star => {
                    star.classList.remove("glow");
                });
            }
        });

        star.addEventListener("click", function() {
            selectedRating = index + 1; // 更新当前选择的评分值
            console.log(selectedRating)
            for (let i = 0; i < stars.length; i++) {
                if (i <= index) {
                    stars[i].classList.add("glow");
                } else {
                    stars[i].classList.remove("glow");
                }
            }
            document.querySelector("input[name='stars']").value = selectedRating;
        });
    });
});


