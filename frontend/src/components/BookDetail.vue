<template>
      <div class="container">
              <h1>Book detail</h1>
              <h3>{{ book.title }}</h3>
              <div v-if="book.cover" class="photo-container">
                <img :src="book.cover"
                     height="400px"
                     width="300px"/>
              </div>
              <p>Authors:
                <ul v-for="author in book.authors">
                  <li>{{ author.short_name }}</li>
                </ul>
              <p>Genre:
                  <ul for v-for="g in book.genre">
                    <li>{{ g.name }}</li>
                  </ul>
              </p>
              <p>Year: {{ book.year }}</p>
              <p>Count of pages: {{ book.number_page }}</p>
              <p>Publisher: {{ book.publishing.name }}</p>
              <p>Description: {{ book.description }}</p>
      </div>
</template>
<script>
  import {APIService} from '../http/ApiService';
  const apiService = new APIService();

  export default {
      name: 'BookDetail',
      data() {
          return {
              book: [],
              id: 0
          };
       },
      methods: {
          getDetail(){
              this.loading = true;
              this.id = this.$route.params.id;
              apiService.getBook(this.$route.params.id ).then((book) => {
                  this.book = book;
                  console.log(book);
                  this.loading = false;
              });
            }
      },
  mounted() {
      this.getDetail();
  },
 }
</script>
