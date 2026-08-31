# Net naming conventions

Use stable functional names across KiCad, WireViz, firmware comments/config, and
interface records. Prefer these patterns:

| Pattern | Meaning / examples |
| --- | --- |
| `GND`, `PGND`, `CHASSIS` | Do not merge distinct return/chassis domains casually |
| `VBAT`, `VBUS_USB`, `VRAW` | Unregulated or source-side power |
| `+5V_SYS`, `+3V3`, `+1V8` | Regulated rails; suffix switched rails, e.g. `+3V3_SENS` |
| `I2C1_SDA`, `I2C1_SCL` | Bus plus instance when more than one can exist |
| `SPI1_SCK`, `SPI1_MOSI` | Use one spelling across all artifacts |
| `SENSOR_INT_N`, `LOAD_EN` | Active-low signals end in `_N` |
| `UART0_TX_CTRL` | Direction is from the named source when ambiguity matters |

Do not use color as the net name. Color belongs to the physical harness. Do not
use `5V` for a rail whose allowed range or source behavior is materially different;
name and annotate it explicitly.
