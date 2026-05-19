const tags = document.querySelectorAll('.filter-tags .tag');

tags.forEach(tag => {
    tag.addEventListener('click', () => {
        tags.forEach(t => t.classList.remove('active'));
        
        tag.classList.add('active');
        
        console.log(`Filtrar conteúdos por: ${tag.textContent}`);
    });
});