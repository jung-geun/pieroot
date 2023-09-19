<script>
    import { time,elapsed } from '../lib/js/time.js';

    const formatter = new Intl.DateTimeFormat('ko-KR', {
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
        hour12: false,
    });
</script>

<div class="container ">
    <h1>This server time is {formatter.format($time)}</h1>
</div>
