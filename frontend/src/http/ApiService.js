import axios from 'axios';
const API_URL = 'http://localhost:8000/api';

export class APIService{
    constructor(){
    }

    getBooks(get_url) {
        const url = API_URL+get_url;
        return axios.get(url).then(response => response.data);
    }
    getBook(id) {
        const url = 'http://localhost:8000/api/books/'+id+'/';
        return axios.get(url).then(response => response.data);
    }
     getBooksByURL(link){
        const url = link;
        return axios.get(url).then(response => response.data);
    }

}
