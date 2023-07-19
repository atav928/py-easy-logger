# easy-logger

Simple Easy baseline Logger. Creates a color stream logger or a basic rotating logger that can be used and called on throughout a project.

## Usage

__Configuration Values:__

* __name:__ Name of file can use built in __\_\_name\_\___ or specifiy a name to call the logger instance.
* __logName:__ filename for log.
* __logDir:__ Directory location to store log.
  * Can use built in utilitiy to find the default log location for the system you are on.
* __level:__ Log Level. Can be one of the following Strings.
  * NOTSET = 0
  * DEBUG = 10
  * INFO = 20
  * WARN = 30
  * WARNING = 30
  * ERROR = 40
  * CRITICAL = 50
  * FATAL = 50
* __setFile:__ Bool Value to set the logger to write out to file.
* __stream:__ Bool Value to allow conosole output of log.
* __maxBytes:__ Maximum Byte size before rotating log file.
* __backupCount:__ Amount of backups to keep.
* __setLog:__ Enables or creates the logging instance otherwise will not log anything.

```python
import easy_logger
from easy_logger.utils import get_log_dir

logger = easy_logger.RotatingLog(__name__,
                                 logName="sample.log",
                                 logDir=get_log_dir(),
                                 level="DEBUG",
                                 stream=True,
                                 setLog=True,
                                 setFile=True,
                                 maxBytes=10000,
                                 backupCount=10)
log = logger.getLogger(__name__)
log.info(f"Writting out file to: {get_log_dir()}")
log.info("This is an informational log message.")
log.debug("This is a debug log message.")
log.warning("This is a warning log message.")
log.critical("This is a critical log message.")

```

What this will look like in the console:

![console output](sample_output.jpg)

If written to file:

```bash
>>> cat ~/Library/Logs/sample.log 
[2023-07-19 12:25:01,648] level=INFO     name=__main__     fn=<ipython-input-1-e1c5bba1549c> ln=14 func=<module>: Writting out file to: /Users/*****/Library/Logs
[2023-07-19 12:25:01,650] level=INFO     name=__main__     fn=<ipython-input-1-e1c5bba1549c> ln=15 func=<module>: This is an informational log message.
[2023-07-19 12:25:01,652] level=DEBUG    name=__main__     fn=<ipython-input-1-e1c5bba1549c> ln=16 func=<module>: This is a debug log message.
[2023-07-19 12:25:01,658] level=WARNING  name=__main__     fn=<ipython-input-1-e1c5bba1549c> ln=17 func=<module>: This is a warning log message.
[2023-07-19 12:25:01,667] level=CRITICAL name=__main__     fn=<ipython-input-1-e1c5bba1549c> ln=18 func=<module>: This is a critical log message.
```

If the __name__ value is passed as a string instead of using the python file name the name will show up in the logs such as:

```python
log = logger.getLogger("easy_logger")
```

```bash
[2023-07-19 12:34:53,266] level=INFO     name=easy_logger  fn=<ipython-input-2-297430e75a74> ln=14 func=<module>: Writting out file to: /Users/*******/Library/Logs
[2023-07-19 12:34:53,268] level=INFO     name=easy_logger  fn=<ipython-input-2-297430e75a74> ln=15 func=<module>: This is an informational log message.
[2023-07-19 12:34:53,268] level=DEBUG    name=easy_logger  fn=<ipython-input-2-297430e75a74> ln=16 func=<module>: This is a debug log message.
[2023-07-19 12:34:53,269] level=WARNING  name=easy_logger  fn=<ipython-input-2-297430e75a74> ln=17 func=<module>: This is a warning log message.
[2023-07-19 12:34:53,269] level=CRITICAL name=easy_logger  fn=<ipython-input-2-297430e75a74> ln=18 func=<module>: This is a critical log message.
```

__NOTE:__ It is usually best practice when passing a logger around a large project to pick up the name of the file and the function for easier troubleshooting depending on what method you use.

## Versions

### v0.0.4

* Added utility to find OS Log directory.
* Added Splunk JSON data formatter.

### v0.0.3

* Added Splunk basic string log out format.
* Added Splunk HEC JSON format for messaging.

## Future Enhancements

* Use a standard or basic logger.
* Allow conversion of int/str types for log level.
