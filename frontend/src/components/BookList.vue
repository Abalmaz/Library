<template>
      <div class="container">
          <div class="row">
              <h1>All books in Library</h1>
              <div class="form-inline my-2 my-lg-0">
                  <input class="form-control mr-sm-2" type="text" placeholder="Search" v-model="search_term" aria-label="Search">
                  <button class="btn btn-outline-success my-2 my-sm-0" v-on:click.prevent="getBooks()">Search</button>
              </div>
              <table class="table">
                  <thead>
                      <tr>
                          <th>Book title</th>
                          <th>Year</th>
                          <th>Authors</th>
                          <th>Genres</th>
                          <th>Rating</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="book in books">
                          <td @click="goToDetail(book.id)">{{ book.title }}</td>
                          <td>{{ book.year }}</td>
                          <td>
                              <ul class="list-unstyled" v-for="author in book.authors">
                                  <li>{{ author.short_name }}</li>
                              </ul>
                          </td>
                          <td>
                              <ul class="list-unstyled" v-for="g in book.genre">
                                  <li>{{ g.name }}</li>
                              </ul>
                          </td>
                          <td>{{ book.rating_avg }}</td>
                      </tr>
                  </tbody>
              </table>
              <div class="loading" v-if="loading===true">Loading&#8230;</div>
              <div>
                  <ul class="pagination justify-content-center">
                    <li class="page-item"><button class="page-link" @click="getPreviousPage()">Previous</button></li>
                    <li class="list-inline-item" v-for="page in pages">
                      <a class="btn btn-primary" @click="getPage(page.link)"></a>
                    </li>
                    <li class="page-item"><button class="page-link" @click="getNextPage()">Next</button></li>
                  </ul>
              </div>
          </div>
      </div>

</template>


<script>
import {APIService} from '../http/ApiService';
const apiService = new APIService();

export default {
  name: 'BookList',
  data() {
      return {
          books: [],
          pages: [],
          numberOfProducts:0,
          loading: false,
          nextPageURL:'',
          previousPageURL:'',
          search_term: ''
      };
   },
  methods: {
    getBooks(){
        let api_url = '/books/';
        if(this.search_term!==''||this.search_term!==null) {
            api_url = '/books/?search='+this.search_term
        }
        this.loading = true;
        apiService.getBooks(api_url).then((page) => {
          this.books = page.results;
          console.log(page);
          console.log(page.next);
          this.numberOfProducts = page.count;
          this.nextPageURL = page.next;
          this.previousPageURL = page.previous;
          this.loading = false;
        });
      },
      getPage(link){
        this.loading = true;
        apiService.getBooksByURL(link).then((page) => {
          this.books = page.results;
          this.nextPageURL = page.next;
          this.previousPageURL = page.previous;
          this.loading = false;
        });
      },
      getNextPage(){
        console.log(this.nextPageURL);
        this.loading = true;
        apiService.getBooksByURL(this.nextPageURL).then((page) => {
          this.books = page.results;
          this.nextPageURL = page.next;
          this.previousPageURL = page.previous;
          this.loading = false;
        });

      },
      getPreviousPage(){
        this.loading = true;
        apiService.getBooksByURL(this.previousPageURL).then((page) => {
          this.books = page.results;
          this.nextPageURL = page.next;
          this.previousPageURL = page.previous;
          this.loading = false;
        });

      },
      goToDetail(book_id) {
        this.$router.push({name:'BookDetail', params:{id:book_id}})
      }
  },
  mounted() {

      this.getBooks();

  },
}
</script>
