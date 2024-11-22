import { createTheme } from '@mui/material/styles';

const theme = createTheme({
    palette: {
        primary: {
            main: '#1976d2', // Customize the primary color
        },
        secondary: {
            main: '#dc004e', // Customize the secondary color
        },
        background: {
            default: '#f4f6f8', // Customize background color
        },
    },
    typography: {
        fontFamily: 'Roboto, Arial, sans-serif', // Default Material-UI font
    },
});

export default theme;