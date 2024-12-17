document.addEventListener('DOMContentLoaded', () => {
    const burger = document.querySelector('.burger');
    const navLinks = document.querySelector('.nav-links');
  
    burger.addEventListener('click', () => {
      // Toggle nav active
      navLinks.classList.toggle('nav-active');
      
      // Toggle burger animation
      burger.classList.toggle('active');
    });
  });