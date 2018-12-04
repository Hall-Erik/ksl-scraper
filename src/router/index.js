import Vue from 'vue';
import Router from 'vue-router';
import Jobs from '@/components/Jobs';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Jobs',
      component: Jobs,
    },
  ],
});
