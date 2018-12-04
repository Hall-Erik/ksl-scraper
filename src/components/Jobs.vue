<template>
  <div class="container-fluid">
    <h1>Jobs from KSL</h1>
    <p v-if="newJobs > 0" class="mb-2">
      Showing {{ jobs.length }} of {{ total }} jobs. ({{ newJobs }} new)
      <b-button class="ml-1 px-1 pt-0 pb-0"
                variant='success'
                size='sm'
                @click="markSeen()">
        Mark all seen
      </b-button>
      <p v-else class="mb-2">
      Showing {{ jobs.length }} of {{ total }} jobs.
      <b-button class="ml-1 px-1 pt-0 pb-0"
                variant='secondary'
                size='sm'
                disabled
                @click="markSeen()">
        Mark all seen
      </b-button>
    </p>
    <div class="media" v-for="(job, index) in jobs" :key='index'
           v-bind:class="{ new: !job.seen}">
        <b-button variant='danger'
                  size='sm'
                  @click="removeJob(job)">
          Hide
        </b-button>
      <div class="media-body ml-2">
        <div class="row">
          <div class="col">
            <a v-bind:href="prefix + job.url" target="_blank">
              {{ job.name }}
            </a>
          </div>
        </div>
        <div class="row">
          <div class="col">
            {{ job.employer }}
          </div>
        </div>
        <div class="row">
          <div class="col">
            {{ job.date_posted }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Scrapyr',
  data() {
    return {
      env: process.env.NODE_ENV,
      prefix: 'https://jobs.ksl.com',
      api_prefix: 'http://192.168.1.66:5000',
      jobs: [],
      total: 0,
      newJobs: 0,
    };
  },
  methods: {
    getJobs() {
      const path = `${this.api_prefix}/api/jobs`;
      axios.get(path)
        .then((res) => {
          this.jobs = res.data.jobs;
          this.total = res.data.total;
          this.countNew();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    countNew() {
      this.newJobs = 0;
      let job;
      // eslint-disable-next-line
      for (job of this.jobs) {
        if (!job.seen) {
          this.newJobs += 1;
        }
      }
    },
    markSeen() {
      const path = `${this.api_prefix}/api/jobs/mark_seen`;
      axios.put(path)
        .then(() => {
          this.getJobs();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    swipeLeftHandler() {
      this.msg = 'Swiped Left';
    },
    swipeRightHandler() {
      this.msg = 'Swiped Right';
    },
    removeJob(job) {
      const path = `${this.api_prefix}/api/jobs/${job.id}/hide`;
      axios.put(path)
        .then(() => {
          // this.$delete(this.jobs, index);
          this.getJobs();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    if (this.env === 'production') {
      this.api_prefix = 'https://career-scraper.herokuapp.com';
    }
    this.getJobs();
  },
};
</script>

<style scoped>
    .new {
        background-color: lightgreen;
    }
</style>
