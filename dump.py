

@click.command()
@click.option('-c', '--clean', default=False, is_flag=True, help='Clear outputs')
def main(period, clean, threshold):
    logger.remove()
    format = "{time:YYYY-MM-DD HH:mm:ss}|{name:10.10s}|{function:10.10s}|{level:4.4s}| {message}"
    logger.add(sys.stdout,  level='DEBUG', format=format)
    logger.add("log.log", level='DEBUG', format=format)
    logger.enable("")

    if clean:
        # remove dir with files
        shutil.rmtree(OUTPUT_PATH)
        OUTPUT_PATH.mkdir(exist_ok=True, parents=True)
    
    func = partial(iteration, threshold)        
    func()        

    if period:
        schedule.every(period).minutes.do(func)
        while True:
            secs = schedule.idle_seconds()
            logger.info(f"Sleeping for {secs} seconds")
            time.sleep(secs)
            schedule.run_pending()
                      
if __name__ == "__main__":
    main()