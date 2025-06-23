module.exports = {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
    ],
    theme: {
        extend: {
            colors: {
                navy: "#03045F",
                deepblue: "#0078B8",
                paleviolet: '#F3E8FF',
                softpink: '#FFE3E3',
                skyblue: '#D6F1FF',
                golden: '#FFEAA7',
                deepviolet: '#7F5AF0',
                lavender: '#D0C4F7',
            },
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
};
