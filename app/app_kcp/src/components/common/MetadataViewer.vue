<template>
  <div>
    <div v-if="metadata.topics_src.concat(metadata.wb_subtopic_src).length > 0">
      <h2>Topics</h2>
      <ul>
        <li
          v-for="topic_name in metadata.topics_src.concat(
            metadata.wb_subtopic_src
          )"
          :key="topic_name"
        >
          {{ topic_name }}
        </li>
      </ul>
    </div>

    {{ metadata }}
  </div>
</template>
<script>
export default {
  props: {
    metadata: Object,
  },
};
</script>
